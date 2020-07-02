#!/usr/bin/env python3

from response.requestHandler import RequestHandler


def get_last_roam_buffer():
    return (
        open("/tmp/aj-org-roam-server-light-last-roam-buffer", "r")
        .read()
        .replace('"', "")
        .rstrip()
    )


class CurrentBufferHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = "text/event-stream"
        self.contents = "data: " + get_last_roam_buffer() + "/n/n"
        self.setStatus(200)

    def getContents(self):
        return self.contents
