#!/usr/bin/env python

import urllib
import os
import mimetypes

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from os.path import basename


HOST = "127.0.0.1"
PORT_NUMBER = 8080
DIR = os.path.expanduser("~/.muttd/message")


class MuttdHandler(BaseHTTPRequestHandler):

    """
    This class will handles any incoming request from the browser.
    """

    def do_GET(self):
        """Handler for the GET requests."""

        if self.path == "/":
            self.path = "/index.html"

        mimetype, _ = mimetypes.guess_type(self.path)
        if not mimetype:
            mimetype = "application/octet-stream"

        # unquote() handles URL encoding and basename is a quick way to
        # avoid users from requesting files outside of the path (for
        # example ../../../../etc/passwd). Not that anybody should be serving
        # muttd on a public IP...
        path = basename(urllib.parse.unquote(self.path))
        try:
            f = open(curdir + sep + path, "rb")
        except IOError:
            self.send_error(404, "File Not Found: {}".format(self.path))
            return
        self.send_response(200)
        self.send_header("Content-type", mimetype)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()


class ServeCommand(object):

    def __init__(self, message_path, address, port):
        self.message_path = message_path
        self.address = address
        self.port = port

    def run(self):
        if not os.path.exists(self.message_path):
            os.makedirs(self.message_path)
        os.chdir(self.message_path)

        server = HTTPServer((self.address, self.port), MuttdHandler)
        print("Started muttd server on http://{}:{}/"
              .format(self.address, self.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("^C received, shutting down the web server")
            server.socket.close()
