#!/usr/bin/env python3

from response.requestHandler import RequestHandler
import json

roam_server_data = ""


class RoamDataHandler(RequestHandler):
    def __init__(self, roam_force):
        super().__init__()
        global roam_server_data

        self.contentType = "text/event-stream"
        new_server_data = json.dumps(json.load(open("query.json")))
        if len(roam_force) > 0:
            is_force = roam_force[0]
        else:
            is_force = False

        if new_server_data == roam_server_data and not is_force:
            self.contents = ""
        else:
            roam_server_data = new_server_data
            self.contents = "data: " + roam_server_data + "\n\n"
        self.setStatus(200)

    def getContents(self):
        return self.contents

    # TODO Write fn for building JSON from real sqlite databased
