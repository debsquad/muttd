#!/usr/bin/env python3.4

"""
Unpack a MIME message into a directory of files.
"""

import os
import sys
import email
import glob
import fileinput
import re
import tarfile
import argparse


template = """
<style>
.muttd {{
    position: fixed;
    top: 0; right: 0;
    transform: translate3d(240px,0,0);
    transition: all .2s ease-out;
    width: 240px;
    height: 100%;
    background: #2E3243;
    font-family: helvetica, sans;
    color: #FFF;
    border-left: 1px solid #1E1F2B;
}}
.muttd.active {{
    transform: translate3d(0,0,0);
    transition: all .2s ease-in;
}}
.muttd .side-cont {{
    padding: 12px 0px;
}}
.muttd a, a:visited {{
    color: inherit;
    outline: 0;
}}
.muttd #muttdmenu {{
    position: absolute;
    top: 0; left: -64px;
    width: 64px;
    height: 64px;
    color: #222;
    text-align: center;
    display: flex;
    -moz-box-align: center;
    align-items: center;
    -moz-box-pack: center;
    justify-content: center;
}}
.muttd .icon-menu {{
    position: absolute;
    display: inline-block;
    top: 28px;
    left: 24px;
    height: 2px;
    width: 24px;
    background: #2E3243;
}}
.muttd .icon-menu:after,
.muttd .icon-menu:before {{
    content: '';
    position: absolute;
    width: 100%;
    height: 2px;
    left: 0;
    background: #2E3243;
}}
.muttd .icon-menu:after {{ top: 6px }}
.muttd .icon-menu:before {{ top: -6px }}
.muttd h2 {{
    font-size: 14px;
    line-height: 48px;
    margin: 0;
    padding: 0 24px;
}}
.muttd .dl-cont {{
    padding: 0 24px;
}}
.muttd a.button {{
    display: block;
    background: #40B1D0;
    border-radius: 2px;
    text-align: center;
    width: 100%;
    line-height: 37px;
    font-size: 14px;
    box-shadow: 0px 2px 2px rgba(0,0,0,.2);
    text-decoration: none;
}}
.muttd a.button:active {{
    box-shadow: none;
    transform: translate3d(0,1px,0);
}}
pre {{
    line-height: 14px;
}}
.muttd .att-cont a,
.muttd .att-cont a:visited {{
    position: relative;
    display: block;
    list-style-type: none;
    padding: 0 24px 0 48px;
    font-size: 13px;
    line-height: 36px;
    color: #BCC1D8;
    text-decoration: none;
}}
.muttd .att-cont a:after {{
    content: "+";
    position: absolute;
    top: 0; left: 24px;
    font-size: 10px;
    font-weight: bold;
    color: #1E1F2B;
}}
.muttd .att-cont a:hover {{
    background: #252736;
    color: #FFF;
}}
.muttd .att-cont a:hover:after {{
    color: #FFF;
}}
</style>
<div class=muttd id=muttd>
    <a href='#' id=muttdmenu>
        <div class='icon-menu'></div>
    </a>
    <div class="side-cont">
        <div class='dl-cont'>
        <a href='/attachments.tgz' class=button>Download <small>(.tgz)</small></a></br>
        </div>
        <div class='att-cont'>
            {}
        </div>
    </div>
</div>
<script type="text/javascript">
function a(){{
    document.querySelector('#muttd').classList.toggle('active');
}}
document.querySelector('#muttdmenu').addEventListener('click', a )
</script>
"""


def main():
    parser = argparse.ArgumentParser(
        description="""\
        Unpack a MIME message into a directory of files inject a list
        of attachments inside .
        """)
    parser.add_argument(
        '-d', '--directory', required=True,
        help="""Unpack the MIME message into the named
        directory, which will be created if it doesn't already
        exist.""")
    parser.add_argument("mailfile", nargs="?", type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()

    msg = email.message_from_file(args.mailfile)

    # Create or clean up folder
    try:
        os.mkdir(args.directory)
    except FileExistsError:
        files = glob.glob(args.directory+'/*')
        for f in files:
            os.remove(f)

    # Init some variables
    htmlList = ""
    attachments = 0
    msgType = 'txt'

    # Unpack our message
    # if our message is multipart, let's unpack it
    if msg.is_multipart():
        for part in msg.walk():
            # skip multipart sub-parts. TODO: parse these as well.
            if part.is_multipart():
                continue
            # save attachments
            if part.get_filename():
                attachments = 1
                filename = part.get_filename()
                with open(os.path.join(args.directory, filename), 'wb') as f:
                    f.write(part.get_payload(decode=True))
                htmlList += "<a href='"+filename+"'>"+filename+"</a>\n"
            # save main message
            else:
                filename = "index.html"
                if part.get_content_charset() is None:
                    text = part.get_payload(decode=True)
                    with open(os.path.join(args.directory, filename), 'wb') as f:
                        f.write(text)
                else:
                    charset = part.get_content_charset()
                    text = str(part.get_payload(decode=True), str(charset),
                               "ignore").encode('utf8', 'replace')
                    with open(os.path.join(args.directory, filename), 'wb') as f:
                        f.write(text)
                    if part.get_content_type() == 'text/html':
                        msgType = 'html'
    # if it's a single part message, let's export it into
    # a single file we will customize later
    else:
        filename = "index.html"
        if msg.get_content_charset() is None:
            with open(os.path.join(args.directory, filename), 'wb') as f:
                f.write(msg.get_payload(decode=True))
        else:
            text = str(msg.get_payload(decode=True), msg.get_content_charset(),
                       'ignore').encode('utf8', 'replace')
            with open(os.path.join(args.directory, filename), 'wb') as f:
                f.write(text)
        if msg.get_content_type() == "text/html":
            msgType = 'html'

    # Compress attachments
    if attachments:
        tar = tarfile.open(os.path.join(args.directory, 'attachments.tgz'), "w:gz")
        tar.add(os.path.join(args.directory))
        tar.close

    # Format index.html
    # any <html> tag already there?
    with open(os.path.join(args.directory, "index.html"), 'r') as f:
        for line in f:
            if re.match("<html>", line):
                htmlTags = 1
                break
            else:
                htmlTags = 0

    count = 0
    for line in fileinput.input(os.path.join(args.directory, "index.html"),
                                inplace=1):
        # add <html> tag when missing
        if count == 0 and msgType == "txt":
            print("<html><pre>")
        elif count == 0 and htmlTags is not 1 and msgType == "html":
            print("<html>")
        if msgType == "html":
            # correct html encoding
            if re.search("charset", line):
                pattern = re.compile('charset=[\sa-z0-9A-Z-]+', re.IGNORECASE)
                line = re.sub(pattern, 'charset=UTF-8', line)
            # add attachment list
            if re.match("</body>", line):
                pattern = re.compile(r'</body>.*$', re.IGNORECASE)
                line = re.sub(pattern, '', line)
                if attachments == 1:
                    print(line+template.format(htmlList))
                else:
                    print(line)
                print("</body></html>")
                break
            elif re.search("</html>", line):
                pattern = re.compile("</html>", re.IGNORECASE)
                line = re.sub(pattern, '', line)
                if attachments == 1:
                    print(line+template.format(htmlList))
                else:
                    print(line)
                print("</html>")
                break
        print(line),
        count += 1

    if attachments == 1:
        if (msgType == "txt"):
            with open(os.path.join(args.directory, "index.html"), 'a') as f:
                f.write("</pre>"+template.format(htmlList)+"</html>")
        if (msgType == "html" and htmlTags is not 1):
            with open(os.path.join(args.directory, "index.html"), 'a') as f:
                f.write(template.format(htmlList)+"</html>")
    else:
        with open(os.path.join(args.directory, "index.html"), 'a') as f:
            f.write("</html>")


if __name__ == '__main__':
    main()
