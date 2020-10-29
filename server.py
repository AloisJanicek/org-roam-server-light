import os
import sqlite3
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from routes.main import routes
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.roamDataHandler import RoamDataHandler
from response.networkVisHandler import NetworkVisHandler
from response.currentBufferHandler import CurrentBufferHandler
from response.filePreviewHandler import FilePreviewHandler
from response.roamBufferHandler import RoamBufferHandler

from variables import org_roam_directory
from variables import org_roam_db


def get_query_field(url, field):
    try:
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []


def get_fullpath(to_be_exported_file):
    conn = sqlite3.connect(org_roam_db)
    c = conn.cursor()
    path_quoted = '"%' + os.path.basename(to_be_exported_file) + '%"'
    query = (
        """
        SELECT file
        FROM files
        WHERE file LIKE '%s'
        """
        % path_quoted
    )
    c.execute(query)
    results = c.fetchall()
    conn.close()
    f = results[0][0].strip('"')
    return f


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        global org_roam_db

        requested_file = os.path.basename(urlparse(self.path)[2])
        requested_extension = os.path.splitext(requested_file)[1]
        requested_filename = os.path.splitext(requested_file)[0]
        to_be_exported_file = os.path.join(
            org_roam_directory, requested_filename + ".org")

        if "network-vis-options" in self.path:
            handler = NetworkVisHandler()

        elif "roam-data" in self.path:
            self.roam_force = get_query_field(self.path, "force")
            handler = RoamDataHandler(self.roam_force, org_roam_db)

        elif "current-buffer-data" in self.path:
            handler = CurrentBufferHandler()

        elif "org-roam-buffer" in self.path:
            file_path = get_query_field(self.path, "path")
            file_label = get_query_field(self.path, "label")
            handler = RoamBufferHandler(org_roam_db, file_path, file_label)

        elif (requested_file
              and requested_extension == ".html"
              and os.path.isfile(to_be_exported_file)):
            handler = FilePreviewHandler(to_be_exported_file, org_roam_db)

        elif (requested_file
              and requested_extension == ".html"
              and os.path.isfile(get_fullpath(to_be_exported_file))):
            handler = FilePreviewHandler(
                get_fullpath(to_be_exported_file), org_roam_db)

        elif requested_extension == "" or requested_extension == ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()

        elif requested_extension == ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(self.path)

        self.respond({"handler": handler})

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code == 200:
            content = handler.getContents()
            self.send_header("Content-type", handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, "UTF-8")

    def respond(self, opts):
        response = self.handle_http(opts["handler"])
        self.wfile.write(response)
