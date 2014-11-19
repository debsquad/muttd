#!/usr/bin/env python3.4

"""
Unpack a MIME message into a directory of files.
"""

import os
import sys
import email
import mimetypes
import glob

from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        description="""\
        Unpack a MIME message into a directory of files.
        """)
    parser.add_argument(
        '-d', '--directory', required=True,
        help="""Unpack the MIME message into the named
        directory, which will be created if it doesn't already
        exist.""")
    args = parser.parse_args()
    source = sys.stdin
    attachlist = "attachments.html"

    # store message
    with source as fp:
        msg = email.message_from_file(fp)

    # create folder
    try:
        os.mkdir(args.directory)
    # or remove previous files
    except FileExistsError:
        files = glob.glob(args.directory+'/*')
        for f in files:
            os.remove(f)
        pass

    # Unpack message
    counter = 1
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        # extract html message
        if part.get_content_type() == 'text/html':
            filename = 'index.html'
            with open(os.path.join(args.directory, filename), 'wb') as fd:
                fd.write(part.get_payload(decode=True))
            continue
        # extract attachments
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = '.bin'
            filename = 'part-%03d%s' % (counter, ext)
        counter += 1
        with open(os.path.join(args.directory, filename), 'wb') as fp:
            fp.write(part.get_payload(decode=True))
        # store attachments list into an html
        with open(os.path.join(args.directory, attachlist), 'a') as fd:
            fd.write("<a href='"+filename+"'>"+filename+"</a>\n")


if __name__ == '__main__':
    main()
