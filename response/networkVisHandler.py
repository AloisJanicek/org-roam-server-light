#!/usr/bin/env python3

import os.path
from response.requestHandler import RequestHandler
from variables import org_roam_server_light_tmp_dir


network_vis_options_file = (
    org_roam_server_light_tmp_dir
    /
    "org-roam-server-light-network-vis-options"
)


class NetworkVisHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        global network_vis_options_file
        self.contentType = "application/json"

        if os.path.isfile(network_vis_options_file) and os.path.getsize(network_vis_options_file) > 0:
            network_vis_options = open(
                network_vis_options_file, "r").read()
            self.contents = network_vis_options
        else:
            self.contents = "{}"

        self.setStatus(200)

    def getContents(self):
        return self.contents
