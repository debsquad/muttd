#!/usr/bin/env python3.4

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

import page


charset_re = re.compile('charset=[\sa-z0-9A-Z-]+', re.IGNORECASE)
messages = []
attachments = []


def process_part(part):
    """Extract the attachment or message within a single part."""
    # This is an attachment, save it on disk and keep track of its name.
    if part.get_filename():
        filename = part.get_filename()
        with open(os.path.join(args.directory, filename), "wb") as f:
            f.write(part.get_payload(decode=True))
        attachments.append(filename)
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

    messages.append(body)


def process_parts(msg):
    """Recursively process message parts and only focus on leafs."""
    process_part(msg)
    parts = list(msg.walk())

    # If the message has both plain and html, skip the plain text.
    content_types = [part.get_content_type() for part in parts]
    if "text/html" in content_types:
         parts = [p for p in parts if p.get_content_type() != "text/plain"]

    for part in parts:
        if msg != part:
            process_parts(part)


def parse_args():
    parser = argparse.ArgumentParser(description="""Unpack a MIME message into a
                                    directory of files inject a list of
                                    attachments inside.""")
    parser.add_argument("-d", "--directory",
                        default=os.path.expanduser("~/.muttd/message"),
                        help="""Unpack the MIME message into the named directory,
                        which will be created if it doesn't already exist.""")
    parser.add_argument("mailfile", nargs="?", type=argparse.FileType("r"),
                        default=sys.stdin)
    return parser.parse_args()


def cleanup_directory(path):
    """Create or clean up folder."""
    try:
        os.makedirs(path)
    except FileExistsError:
        files = glob.glob(os.path.join(path, "*"))
        for f in files:
            os.remove(f)


args = parse_args()
msgdata = args.mailfile.read()
msg = email.message_from_string(msgdata)

cleanup_directory(args.directory)

process_parts(msg)

# Compress attachments
if attachments:
    tar = tarfile.open(os.path.join(args.directory, "attachments.tgz"), "w:gz")
    for attachment in attachments:
        tar.add(os.path.join(args.directory, attachment))
    tar.close()

# Keep a copy of the file for download
with open(os.path.join(args.directory, "email.eml"), "w") as fp:
    fp.write(msgdata)

# Create an index.html to display everything
index_html = page.render(
    subject=msg.get("Subject", "No Subject"),
    messages=messages,
    attachments=attachments,
)
with open(os.path.join(args.directory, "index.html"), "w") as f:
    f.write(index_html)
