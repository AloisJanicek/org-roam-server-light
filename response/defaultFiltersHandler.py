#!/usr/bin/env python3

import os.path
from response.requestHandler import RequestHandler
from variables import org_roam_server_light_tmp_dir


default_include_filters_file = (
    org_roam_server_light_tmp_dir
    /
    "org-roam-server-light-default-include-filters"
)

default_exclude_filters_file = (
    org_roam_server_light_tmp_dir
    /
    "org-roam-server-light-default-exclude-filters"
)


class DefaultFiltersHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        global default_include_filters_file
        global default_exclude_filters_file
        self.contentType = "application/json"

        if (os.path.isfile(default_include_filters_file)
                and os.path.isfile(default_exclude_filters_file)):
            default_include_filters = open(
                default_include_filters_file, "r").read()

            default_exclude_filters = open(
                default_exclude_filters_file, "r").read()

            self.contents = "{\"include\": %s, \"exclude\": %s}" % (
                default_include_filters, default_exclude_filters)
        else:
            self.contents = "{}"

        self.setStatus(200)

    def getContents(self):
        return self.contents
