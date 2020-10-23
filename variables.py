#!/usr/bin/env python3

from os import environ
from sys import platform
from pathlib import Path

if platform == "win32":
    tmp_dir = environ['TMP']
elif platform == "darwin":
    tmp_dir = environ['TMPDIR']
else:
    tmp_dir = '/tmp'

org_roam_server_light_tmp_dir = Path(tmp_dir) / "org-roam-server-light"

org_roam_directory = (org_roam_server_light_tmp_dir /
                      "org-roam-directory").read_text()

org_roam_db = (org_roam_server_light_tmp_dir /
               "org-roam-db-location").read_text()
