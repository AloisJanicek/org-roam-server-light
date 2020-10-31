#!/usr/bin/env python3

import os.path
from response.requestHandler import RequestHandler
from variables import org_roam_server_light_tmp_dir


server_css_file = (
    org_roam_server_light_tmp_dir
    /
    "org-roam-server-light-style"
)


class ServerCSSHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        global server_css_file
        self.contentType = "text/css"

        if (os.path.isfile(server_css_file)
                and os.path.isfile(server_css_file)):
            server_css = open(
                server_css_file, "r").read()

            self.contents = server_css
        else:
            self.contents = ""

        self.setStatus(200)

    def getContents(self):
        return self.contents
