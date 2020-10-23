import os
import sqlite3
from response.requestHandler import RequestHandler
from variables import org_roam_server_light_tmp_dir


class FilePreviewHandler(RequestHandler):
    def __init__(self, to_be_exported_file, org_roam_db):
        super().__init__()
        self.contentType = "text/html"
        self.to_be_exported_file = to_be_exported_file
        self.export_dir = org_roam_server_light_tmp_dir
        self.org_roam_db = org_roam_db
        self.filename = os.path.basename(to_be_exported_file).rstrip(".org")
        self.exported_file = self.export_dir + self.filename + ".html"
        os.system(
            "pandoc "
            + to_be_exported_file
            + " "
            + "-f org "
            + "-t html "
            + "-o "
            + self.exported_file
        )
        with open(self.exported_file, "r+") as f:
            body = f.read()
            f.seek(0)
            f.write(
                """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="utf-8">
                </head>
                <body>
                <br>
                """
                + "<h1>"
                + self.get_title()
                + "</h1>"
                + body
                + """
                </body>
                </html>
                """
            )

        self.fix_href()
        self.contents = open(self.exported_file)
        self.setStatus(200)

    def fix_href(self):
        f = open(self.exported_file, "r")
        d = f.read()
        d = d.replace('.org">', '.html">')
        f.close()
        f = open(self.exported_file, "w")
        f.write(d)
        f.close()

    def get_title(self):
        conn = sqlite3.connect(self.org_roam_db)
        c = conn.cursor()
        path_quoted = '"' + self.to_be_exported_file + '"'
        query = (
            """
            SELECT title
            FROM titles
            WHERE file = '%s'
            """
            % path_quoted
        )
        c.execute(query)
        results = c.fetchall()
        conn.close()
        title = results[0][0].strip('"')

        return title
