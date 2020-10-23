#!/usr/bin/env python3

import os.path
from response.requestHandler import RequestHandler
from variables import org_roam_server_light_tmp_dir

last_roam_buffer_file = (
    org_roam_server_light_tmp_dir
    /
    "org-roam-server-light-last-roam-buffer"
)

previous_mtime = 1


class CurrentBufferHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        global last_roam_buffer_file
        global previous_mtime

        self.contentType = "text/event-stream"

        if os.path.isfile(last_roam_buffer_file):
            current_mtime = os.path.getmtime(last_roam_buffer_file)
            if current_mtime == previous_mtime:
                self.contents = ""
            else:
                last_roam_buffer = open(last_roam_buffer_file, "r").read()
                self.contents = "data: " + last_roam_buffer + "\n\n"
                previous_mtime = current_mtime
        else:
            self.contents = ""
        self.setStatus(200)

    def getContents(self):
        return self.contents
