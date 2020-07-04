#!/usr/bin/env python3

import os.path
from response.requestHandler import RequestHandler


class CurrentBufferHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = "text/event-stream"
        last_roam_buffer_file = (
            "/tmp/org-roam-server-light/aj-org-roam-server-light-last-roam-buffer"
        )
        if os.path.isfile(last_roam_buffer_file):
            last_roam_buffer = open(last_roam_buffer_file, "r").read()
            self.contents = "data: " + last_roam_buffer + "\n\n"
        else:
            self.contents = ""
        self.setStatus(200)

    def getContents(self):
        return self.contents
