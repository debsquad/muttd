#!/usr/bin/env python3.4

"""Unpack and store a MIME message into memory."""

import sys
import email
import mimetypes
from array import *

def main():
    source = sys.stdin
	
    # store message
    with source as fp:
        msg = email.message_from_file(fp)
    
    # Unpack message
    counter = 1
    htmlList = ""
    for part in msg.walk():
        # skip multipart/* which are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        # Extract html part of the message and store it into an array 
        # conventionally named "aList[index.html]", called later by our
        # http daemon
        if part.get_content_type() == 'text/html':
            fname = 'index.html'
            ftype = part.get_content_type()
            fdata = part.get_payload(decode=True)
            aList = {
                fname: [fname, ftype, fdata],
            }
            continue
        # Extract attachments and store them into arrays conventionally
        # named "aList[filename]"
        fname = part.get_filename()
        if not fname:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = '.bin'
            fname = 'part-%03d%s' % (counter, ext)
            ftype = 'application/octet-stream'
        else:
            ftype = part.get_content_type()
        counter += 1
        fdata = part.get_payload(decode=True)
        aList = {
            fname: [fname, ftype, fdata],
        }
        # Store attachment(s) into an html list
        htmlList = htmlList.join(["<a href='"+fname+"'>"+fname+"</a>\n"])

if __name__ == '__main__':
    main()
