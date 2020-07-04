import os
from response.requestHandler import RequestHandler


class FilePreviewHandler(RequestHandler):
    def __init__(self, to_be_exported_file):
        super().__init__()
        self.contentType = "text/html"

        export_dir = "/tmp/org-roam-server-light/"
        filename = os.path.basename(to_be_exported_file).rstrip(".org")
        exported_file = export_dir + filename + ".html"
        os.system(
            "pandoc "
            + to_be_exported_file
            + " "
            + "-f org "
            + "-t html "
            + "-o "
            + exported_file
        )
        with open(exported_file, "r+") as f:
            body = f.read()
            f.seek(0)
            f.write(
                """
                <!DOCTYPE html>
                <html class="no-js" lang="en">
                <head>
                <meta charset="utf-8">
                </head>
                <body>
                """
                + body
                + """
                </body>
                </html>
                """
            )
        self.contents = open(exported_file)
        self.setStatus(200)
