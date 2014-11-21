#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep


HOST = "127.0.0.1"
PORT_NUMBER = 8080


class MuttdHandler(BaseHTTPRequestHandler):

    """
    This class will handles any incoming request from the browser.
    """

    def do_GET(self):
        """Handler for the GET requests."""

        if self.path == "/":
            self.path = "/index.html"

        try:
            # Check the file extension required and set the right mime type

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

            if sendReply:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, "File Not Found: {}".format(self.path))

try:
    # Create a web server and define the handler to manage the incoming request
    server = HTTPServer((HOST, PORT_NUMBER), MuttdHandler)
    print("Started httpserver on port {}".format(PORT_NUMBER))

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()
