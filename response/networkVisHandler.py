#!/usr/bin/env python3

from response.requestHandler import RequestHandler


class NetworkVisHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = "application/json"
        self.contents = "{}"
        self.setStatus(200)

    def getContents(self):
        return self.contents
