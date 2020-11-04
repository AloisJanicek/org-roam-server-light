#!/usr/bin/env python3
import time
import sys
from http.server import HTTPServer
from server import Server

HOST_NAME = "localhost"
PORT_NUMBER = 8080


class QuietHandler(Server):
    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == '-d':
        httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    else:
        httpd = HTTPServer((HOST_NAME, PORT_NUMBER), QuietHandler)
        print(
            "If you want to see full request log, pass '-d' debug switch to this program.")
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
