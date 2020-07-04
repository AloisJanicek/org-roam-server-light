#!/usr/bin/env python3

import os
import json
import sqlite3
import urllib.parse
from response.requestHandler import RequestHandler


org_roam_directory = open("/tmp/org-roam-server-light/org-roam-directory", "r").read()

org_roam_db = org_roam_directory + "/org-roam.db"


def roam_server_data():

    graph = {"nodes": [], "edges": []}

    conn = sqlite3.connect(org_roam_db)

    c = conn.cursor()

    node_query = """SELECT titles.file,titles,tags
                    FROM titles
                    LEFT OUTER JOIN tags
                    ON titles.file = tags.file"""
    c.execute(node_query)
    nodes = c.fetchall()

    for node in nodes:
        d = {}
        path = node[0].strip('"')
        d["id"] = os.path.splitext(os.path.basename(path))[0]
        title = node[1].rstrip(')"').lstrip('("')
        d["title"] = title
        d["tags"] = node[2]
        d["label"] = title
        d["url"] = "org-protocol://roam-file?file=" + urllib.parse.quote_plus(path)
        d["path"] = path
        graph["nodes"].append(d)

    edges_query = """WITH selected AS (SELECT file FROM files)
                    SELECT DISTINCT [from],[to]
                    FROM links
                    WHERE [to] IN selected AND [from] IN selected"""
    c.execute(edges_query)
    edges = c.fetchall()

    for edge in edges:
        d = {}
        striped_from = edge[0].rstrip(')"').lstrip('("')
        striped_to = edge[1].rstrip(')"').lstrip('("')
        d["from"] = os.path.splitext(os.path.basename(striped_from))[0]
        d["to"] = os.path.splitext(os.path.basename(striped_to))[0]
        d["arrows"] = None
        graph["edges"].append(d)

    conn.close()
    return json.dumps(graph, ensure_ascii=False)


previous_results = ""


class RoamDataHandler(RequestHandler):
    def __init__(self, roam_force):
        super().__init__()
        global previous_results
        self.contentType = "text/event-stream"
        if len(roam_force) > 0:
            is_force = roam_force[0]
        else:
            is_force = False

        new_results = roam_server_data()
        if previous_results == new_results and not is_force:
            self.contents = ""
        else:
            previous_results = new_results
            self.contents = "data: " + new_results + "\n\n"

        self.setStatus(200)

    def getContents(self):
        return self.contents
