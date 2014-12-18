#!/usr/bin/env python

import urllib
import os

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
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

        sendReply = False
        if self.path.endswith(".txt"):
            mimetype = "text/plain"
            sendReply = True
        elif self.path.endswith(".html"):
            mimetype = "text/html"
            sendReply = True
        elif self.path.endswith(".jpg"):
            mimetype = "image/jpg"
            sendReply = True
        elif self.path.endswith(".gif"):
            mimetype = "image/gif"
            sendReply = True
        elif self.path.endswith(".png"):
            mimetype = "image/png"
            sendReply = True
        elif self.path.endswith(".js"):
            mimetype = "application/javascript"
            sendReply = True
        elif self.path.endswith(".css"):
            mimetype = "text/css"
            sendReply = True

        if not sendReply:
            mimetype = "application/octet-stream"
            sendReply = True

        # Open the static file requested and send it
        if sendReply:
            # unquote() handles URL encoding and basename is a quick way to
            # avoid users from requesting files outside of the path (for
            # example ../../../../etc/passwd)
            path = basename(urllib.unquote(self.path))
            try:
                f = open(curdir + sep + path)
            except IOError:
                self.send_error(404, "File Not Found: {}".format(self.path))
                return
            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()


if not os.path.exists(DIR):
    os.makedirs(DIR)
    os.chdir(DIR)

# Create a web server and define the handler to manage the incoming request
server = HTTPServer((HOST, PORT_NUMBER), MuttdHandler)
print("Started httpserver on port {}".format(PORT_NUMBER))

try:
    # Wait forever for incoming http requests
    server.serve_forever()
except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()
