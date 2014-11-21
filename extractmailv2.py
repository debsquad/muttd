#!/usr/bin/env python3.4

"""
Unpack a MIME message into a directory of files.
"""

import os
import sys
import email
import errno
import mimetypes
import glob
import fileinput
import re

from argparse import ArgumentParser

template = """                                                                      
<style>
.menu {{
    position: fixed;
    top: 0; right: 0;
    width: 48px;
    height: 48px;
    background: #000;
    color: #FFF;
    text-align: center;
    display: flex;
    -moz-box-align: center;
    align-items: center;
    -moz-box-pack: center;
    justify-content: center;
}}
.border-menu {{
    position: relative;
    display: inline-block;
    width: 1em;
    height: 1em;
}}
.border-menu:before {{
    content: '';
    position: absolute;
    top: 0.25em;
    left: 0;
    width: 1em;
    height: 0.125em;
    border-top: 0.375em double #fff;
    border-bottom: 0.125em solid #fff;
}}
</style>
<a href='#'  class=menu>
	<div class='border-menu'>
	</div>
</a>
{}
"""

def main():
    parser = ArgumentParser(
        description="""\
        Unpack a MIME message into a directory of files inject a list
        of attachments inside .
        """)
    parser.add_argument(
        '-d', '--directory', required=True,
        help="""Unpack the MIME message into the named
        directory, which will be created if it doesn't already
        exist.""")
    args = parser.parse_args()
    source = sys.stdin

    # get email from stdin
    with source as fp:
        msg = email.message_from_file(fp)

    # create or clean up folder
    try:
        os.mkdir(args.directory)
    except FileExistsError:
        files = glob.glob(args.directory+'/*')
        for f in files:
            os.remove(f)
        pass
    
    htmlList = ""
    # unpack message: case multipart
    if msg.is_multipart():
        for part in msg.walk():
            # skip multipart/*
            if part.get_content_maintype() == 'multipart':
                continue

            # save attachments
            if part.get_filename():
                filename = part.get_filename()
                with open(os.path.join(args.directory, filename), 'wb') as fp:
                    fp.write(part.get_payload(decode=True))
                htmlList = htmlList+"<a href='"+filename+"'>"+filename+"</a>\n"

            # save main message
            else:
                filename = "index.html"
                if part.get_content_charset() is None:
                    text = part.get_payload(decode=True)
                    with open(os.path.join(args.directory, filename), 'wb') as fd:
                        fd.write(part.get_payload(decode=True))
                    continue
                charset = part.get_content_charset()
                if part.get_content_type() == "text/plain":
                    text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    with open(os.path.join(args.directory, filename), 'wb') as fd:
                        fd.write(text)
                    msgType = 'txt'    
                    continue
                if part.get_content_type() == 'text/html':
                    html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                    with open(os.path.join(args.directory, filename), 'wb') as fd:
                        fd.write(html)
                    msgType = 'html'
                    continue

    # other case: single message                
    else:
        filename = "index.html"
        if msg.get_content_charset() is None:
            text = msg.get_payload(decode=True)
        else:    
            text = str(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        with open(os.path.join(args.directory, filename), 'wb') as fd:
            fd.write(text)
        if msg.get_content_type() == "text/html":
            msgType = 'html'
        else:
            msgType = 'txt'

    # check if our file has <html> tags (need to be improved)
    for line in fileinput.input(
        os.path.join(args.directory, "index.html"), inplace=1):
        print(line)
        if re.match("<html>", line):
            htmlTags = 1
        else:
            htmlTags = 0
    
    # Format index.html
    count = 0
    for line in fileinput.input(
        os.path.join(args.directory, "index.html"), inplace=1):
        # add <html> tag when missing
        if count == 0 and msgType == "txt":
            print("<html><pre>")
        elif count == 0 and htmlTags is not 1 and msgType == "html":
            print("<html>")
        # add attachment list
        if msgType == "html" and re.match("</body>", line):
            pattern = re.compile("</body>", re.IGNORECASE)
            line = re.sub(pattern, '', line)
            print(line+template.format(htmlList))
            print("</body></html>")				
            break
        elif msgType == "html" and re.search("</html>", line):
            pattern = re.compile("</html>", re.IGNORECASE)
            line = re.sub(pattern, '', line)
            print(line+template.format(htmlList))
            print("</html>")
            break
        print(line),
        count += 1
    if (msgType == "txt"):
        with open(os.path.join(args.directory, "index.html"), 'a') as fp:
            fp.write("</pre>"+template.format(htmlList)+"</html>")
    if (msgType == "html" and htmlTags is not 1):
        with open(os.path.join(args.directory, "index.html"), 'a') as fp:
            fp.write(template.format(htmlList)+"</html>")


if __name__ == '__main__':
    main()
