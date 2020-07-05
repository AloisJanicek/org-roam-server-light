import os
from response.requestHandler import RequestHandler


class FilePreviewHandler(RequestHandler):
    def __init__(self, to_be_exported_file):
        super().__init__()
        self.contentType = "text/html"

        self.export_dir = "/tmp/org-roam-server-light/"
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
