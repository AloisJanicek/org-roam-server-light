#!/usr/bin/env python3

from response.requestHandler import RequestHandler


class CurrentBufferHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = "text/event-stream"
        last_roam_buffer = open(
            "/tmp/org-roam-server-light/aj-org-roam-server-light-last-roam-buffer", "r"
        )
        self.contents = "data: " + last_roam_buffer.read() + "\n\n"
        self.setStatus(200)

    def getContents(self):
        return self.contents
