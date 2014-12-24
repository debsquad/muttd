#!/usr/bin/env python3.4

template = """
<html>
<head>
    <title>muttd - {subject}</title>
    <meta charset="UTF-8">
</head>
<body>
<div id="messages">
    {messages}
</div>
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
            <a href='/email.eml' class=button>Raw email <small>(.eml)</small></a></br>
            {all_attachments_button}
        </div>
        <div class='att-cont'>
            {attachments}
        </div>
    </div>
</div>
<script type="text/javascript">
function a(){{
    document.querySelector('#muttd').classList.toggle('active');
}}
document.querySelector('#muttdmenu').addEventListener('click', a )
</script>
</body>
</html>
"""


def render(subject, messages, attachments):
    if attachments:
        attachments = ["<a href=\""+f+"\">"+f+"</a>" for f in attachments]
        all_attachments_button = ("<a href='/attachments.tgz' class=button>"
                                  "All attachment <small>(.tgz)</small></a>"
                                  "</br>")
    else:
        attachments = ""
        all_attachments_button = ""

    messages = "\n".join(messages)

    return template.format(
        subject=subject,
        all_attachments_button=all_attachments_button,
        attachments="\n".join(attachments),
        messages=messages,
    )
