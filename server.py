import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from routes.main import routes
from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.roamDataHandler import RoamDataHandler
from response.networkVisHandler import NetworkVisHandler
from response.currentBufferHandler import CurrentBufferHandler


def get_query_field(url, field):
    try:
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []


# get_query_field("/roam-data?force=1&token=null", "force")


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if "network-vis-options" in self.path:
            handler = NetworkVisHandler()

        elif "roam-data" in self.path:
            self.roam_force = get_query_field(self.path, "force")
            handler = RoamDataHandler(self.roam_force)

        elif "current-buffer-data" in self.path:
            handler = CurrentBufferHandler()

        elif request_extension == "" or request_extension == ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        elif request_extension == ".py":
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
