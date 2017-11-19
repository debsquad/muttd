# Copyright (c) 2017 Bertrand Janin <b@janin.com>
# Copyright (c) 2015 Vincent Tantardini, Bertrand Janin
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""muttd server command and HTTP request handler.

Command serving the email files via HTTP.
"""


import urllib
import os
import mimetypes

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from os.path import basename


class MuttdRequestHandler(BaseHTTPRequestHandler):

    """
    Handle any incoming request from the browser.
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

    """
    Create an HTTP server with the message path as root directory.
    """

    def __init__(self, message_path, address, port):
        self.message_path = message_path
        self.address = address
        self.port = port

    def run(self):
        if not os.path.exists(self.message_path):
            os.makedirs(self.message_path)
        os.chdir(self.message_path)

        server = HTTPServer((self.address, self.port), MuttdRequestHandler)
        print("Started muttd server on http://{}:{}/"
              .format(self.address, self.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("^C received, shutting down the web server")
            server.socket.close()
