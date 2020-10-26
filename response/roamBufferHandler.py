import os

import sqlite3

from response.requestHandler import RequestHandler


class RoamBufferHandler(RequestHandler):
    def __init__(self, org_roam_db, path, label):
        super().__init__()
        self.org_roam_db = org_roam_db
        self.contentType = "text/html"

        self.contents = (
            """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="utf-8">
            <style>
            a {color: #0062CC;}
            * {font-size: 1.1rem;}
            </style>
            </head>
            <body>
            <br>
            """
            + "<br>"
            + "<p>"
            + label[0]
            + "</p"
            + "<br>"
            + self.get_backlinks(path)
            + """
            </body>
            </html>
            """
        )
        self.setStatus(200)

    def getContents(self):
        return self.contents

    def get_backlinks(self, path):
        conn = sqlite3.connect(self.org_roam_db)
        c = conn.cursor()

        path_quoted = '"' + path[0] + '"'
        query = (
            """
            SELECT [source], title, [dest], [properties]
            FROM links
            LEFT OUTER JOIN titles
            ON titles.file = [source]
            WHERE [dest] = '%s'
            """
            % path_quoted
        )
        c.execute(query)
        results = c.fetchall()
        conn.close()

        html = ""
        for item in results:
            file_title = item[1].strip('"')
            file_id = os.path.basename(item[0])
            file_backlinks = item[3].split("[[file:")
            backlinks_html = (
                '<div class="outline-3">'
                + "<h3>"
                + '<a name="backlink" id="'
                + file_id
                + ' href="javascript:void(0)">'
                + file_title
                + "</a>"
                + "</h3>"
                + '<div class="outline-text-3"><p>'
            )
            for backlink_str in file_backlinks:

                try:
                    backlink_str[0: backlink_str.index("]]")]
                except Exception:
                    continue

                backlink_str = backlink_str[0: backlink_str.index(
                    "]]")].split("][")
                backlink_id = os.path.basename(backlink_str[0])
                backlink_title = backlink_str[1]
                backlinks_html = (
                    backlinks_html
                    + '<a name="backlink" id="'
                    + backlink_id
                    + '" href="javascript:void(0)">'
                    + backlink_title
                    + "</a>"
                    + " "
                )
            backlinks_html = backlinks_html + "</p></div></div>"
            html = html + backlinks_html

        return html
