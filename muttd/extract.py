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

"""
Unpack a MIME message into a directory of files.
"""

import cgi
import os
import sys
import email
import glob
import re
import tarfile
import argparse

from . import page


charset_re = re.compile('charset=[\sa-z0-9A-Z-]+', re.IGNORECASE)


class ExtractCommand(object):

    def __init__(self, message_path):
        self.message_path = message_path
        self.messages = []
        self.attachments = []
        self.inline_images = {}

    def _process_part(self, part):
        """Extract the attachment or message within a single part."""
        # This is an attachment, save it on disk and keep track of its name.
        if part.get_filename():
            filename = part.get_filename().replace("\n", "")
            with open(os.path.join(self.message_path, filename), "wb") as f:
                f.write(part.get_payload(decode=True))
            self.attachments.append(filename)
            # This is an inline attachment, store its cid and filename.
            cid = part.get('Content-ID')
            if cid:
                # cids are wrapped in <>
                self.inline_images[cid[1:-1]] = filename
            return

        # Ignore any part that doesn't contain data
        payload = part.get_payload(decode=True)
        if not payload:
            return

        # Ignore any part that isn't text.
        content_type = part.get_content_type()
        if not content_type.startswith("text/"):
            return

        content_charset = part.get_content_charset()
        if not content_charset:
            content_charset = "UTF-8"

        body = payload.decode(content_charset, "replace")

        if content_type == "text/plain":
            body = "<pre>{}</pre>".format(cgi.escape(body))
        elif content_type == "text/html":
            body = re.sub(charset_re, "charset=UTF-8", body)

        self.messages.append(body)

    def _process_parts(self, msg):
        """Recursively process message parts and only focus on leafs."""
        self._process_part(msg)
        parts = list(msg.walk())

        # If the message has both plain and html, skip the plain text.
        content_types = [part.get_content_type() for part in parts]
        if "text/html" in content_types:
            parts = [p for p in parts if p.get_content_type() != "text/plain"]

        for part in parts:
            if msg != part:
                self._process_parts(part)

    def _cleanup_message_path(self):
        """Create or clean up folder."""
        try:
            os.makedirs(self.message_path)
        except FileExistsError:
            files = glob.glob(os.path.join(self.message_path, "*"))
            for f in files:
                os.remove(f)

    def run(self):
        fp = open("/Users/bertrand/tmp/inbox/cur/1483313342.91470_0.prometheus.tamentis.com:2,S")
        # msgdata = sys.stdin.read()
        msgdata = fp.read()
        msg = email.message_from_string(msgdata)

        self._cleanup_message_path()
        self._process_parts(msg)

        # Compress attachments
        if self.attachments:
            tar = tarfile.open(os.path.join(self.message_path, "attachments.tgz"), "w:gz")
            for attachment in self.attachments:
                tar.add(os.path.join(self.message_path, attachment))
            tar.close()

        # Inline images
        if self.inline_images:
            for idx, i in enumerate(self.messages):
                for p in sorted(self.inline_images.keys()):
                    self.messages[idx] = messages[idx].replace(
                        'cid:' + p,
                        self.inline_images[p],
                    )

        # Keep a copy of the file for download
        with open(os.path.join(self.message_path, "email.eml"), "w") as fp:
            fp.write(msgdata)

        # Create an index.html to display everything
        index_html = page.render(
            subject=msg.get("Subject", "No Subject"),
            messages=self.messages,
            attachments=self.attachments,
        )
        with open(os.path.join(self.message_path, "index.html"), "w") as f:
            f.write(index_html)
