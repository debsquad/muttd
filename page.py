#!/usr/bin/env python3.4

header = """
<!DOCTYPE html>
<html>
<head>
    <title>muttd - {subject}</title>
    <meta charset="UTF-8">
"""

footer = """
</body>
</html>
"""

body = """
</head>

<body>
<div class="menu-wrap">
    <nav class=menu>
        <div class="icon-list">
            {attachments}
            {all_attachments_button}
            <a href='/email.eml'>
                <i class="icon-mail"></i>Raw email <small>(.eml)</small>
            </a>
        </div>
        <button class="close-button" id="close-button">Close Menu</button>
    </nav>
</div>

<button class="menu-button" id="open-button">Open Menu</button>

<div class="content-wrap">
    <div class=content>
        {messages}
    </div>
</div>
"""

scripts = """
<script type="text/javascript">
function toggle_menu(){{
    document.querySelector('body').classList.toggle('show-menu');
}}
document.querySelector('#open-button').addEventListener('click', toggle_menu )
document.querySelector('#close-button').addEventListener('click', toggle_menu )
</script>
"""

normalize = """
<style>
article,aside,details,figcaption,figure,footer,header,hgroup,main,nav,section,summary{{display:block;}}audio,canvas,video{{display:inline-block;}}audio:not([controls]){{display:none;height:0;}}[hidden]{{display:none;}}html{{font-family:sans-serif;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;}}body{{margin:0;}}a:focus{{outline:thin dotted;}}a:active,a:hover{{outline:0;}}h1{{font-size:2em;margin:0.67em 0;}}abbr[title]{{border-bottom:1px dotted;}}b,strong{{font-weight:bold;}}dfn{{font-style:italic;}}hr{{-moz-box-sizing:content-box;box-sizing:content-box;height:0;}}mark{{background:#ff0;color:#000;}}code,kbd,pre,samp{{font-family:monospace,serif;font-size:1em;}}pre{{white-space:pre-wrap;}}q{{quotes:"\201C" "\201D" "\2018" "\2019";}}small{{font-size:80%;}}sub,sup{{font-size:75%;line-height:0;position:relative;vertical-align:baseline;}}sup{{top:-0.5em;}}sub{{bottom:-0.25em;}}img{{border:0;}}svg:not(:root){{overflow:hidden;}}figure{{margin:0;}}fieldset{{border:1px solid #c0c0c0;margin:0 2px;padding:0.35em 0.625em 0.75em;}}legend{{border:0;padding:0;}}button,input,select,textarea{{font-family:inherit;font-size:100%;margin:0;}}button,input{{line-height:normal;}}button,select{{text-transform:none;}}button,html input[type="button"],input[type="reset"],input[type="submit"]{{-webkit-appearance:button;cursor:pointer;}}button[disabled],html input[disabled]{{cursor:default;}}input[type="checkbox"],input[type="radio"]{{box-sizing:border-box;padding:0;}}input[type="search"]{{-webkit-appearance:textfield;-moz-box-sizing:content-box;-webkit-box-sizing:content-box;box-sizing:content-box;}}input[type="search"]::-webkit-search-cancel-button,input[type="search"]::-webkit-search-decoration{{-webkit-appearance:none;}}button::-moz-focus-inner,input::-moz-focus-inner{{border:0;padding:0;}}textarea{{overflow:auto;vertical-align:top;}}table{{border-collapse:collapse;border-spacing:0;}}
</style>
"""

icons = """
<style>
@font-face {{
    font-family: 'fontello';
    src: url('data:application/octet-stream;base64,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') format('woff'),
    url('data:application/octet-stream;base64,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') format('truetype');
}}
[class^="icon-"]:before, [class*=" icon-"]:before {{
    font-family: "fontello";
    font-style: normal;
    font-weight: normal;
    speak: none;

    display: inline-block;
    text-decoration: inherit;
    width: 1.28571em;
    text-align: center;
    font-variant: normal;
    text-transform: none;
    line-height: 1em;
    margin-right: .4em;
}}
.icon-download:before {{ content: '\e800'; }} /* '' */
.icon-file-archive:before {{ content: '\e801'; }} /* '' */
.icon-mail:before {{ content: '\e802'; }} /* '' */
</style>
"""

styles = """
<style>
*, *:after, *:before {{ -webkit-box-sizing: border-box; box-sizing: border-box; }}
.clearfix:before, .clearfix:after {{ content: ''; display: table; }}
.clearfix:after {{ clear: both; }}

body {{
    font-weight: 400;
    font-size: 1em;
    font-family: Arial, sans-serif;
    background: white!important;
}}

a {{
    color: #4e4a46;
    text-decoration: none;
    outline: none;
}}

a:hover, a:focus {{
    color: #c94e50;
    outline: none;
}}

button:focus {{
    outline: none;
}}

html, 
body, 
.content-wrap {{
	overflow: hidden;
	width: 100%;
	height: 100%;
        box-sizing: padding-box;
}}

.content > pre {{
    margin: 0;
}}

.menu-wrap a {{
	color: #b8b7ad;
}}

.menu-wrap a:hover,
.menu-wrap a:focus {{
	color: #c94e50;
}}

.content-wrap {{
    overflow-y: scroll;
    -webkit-overflow-scrolling: touch;
}}

.content {{
    position: relative;
    min-height: 100%;
    padding: 36px 114px 0;
}}

.content::before {{
	position: absolute;
	top: 0;
	left: 0;
	z-index: 10;
	width: 100%;
	height: 100%;
	background: rgba(0,0,0,0.3);
	content: '';
	opacity: 0;
	-webkit-transform: translate3d(100%,0,0);
	transform: translate3d(100%,0,0);
	-webkit-transition: opacity 0.4s, -webkit-transform 0s 0.4s;
	transition: opacity 0.4s, transform 0s 0.4s;
	-webkit-transition-timing-function: cubic-bezier(0.7,0,0.3,1);
	transition-timing-function: cubic-bezier(0.7,0,0.3,1);
}}

/* Menu Button */
.menu-button {{
	position: fixed;
	z-index: 1000;
	margin: 1em;
	padding: 0;
	width: 2.5em;
	height: 2.25em;
	border: none;
	text-indent: 2.5em;
	font-size: 1.5em;
	color: transparent;
	background: transparent;
}}

.menu-button::before {{
	position: absolute;
	top: 0.5em;
	right: 0.5em;
	bottom: 0.5em;
	left: 0.5em;
	background: linear-gradient(#373a47 20%, transparent 20%, transparent 40%, #373a47 40%, #373a47 60%, transparent 60%, transparent 80%, #373a47 80%);
	content: '';
}}

.menu-button:hover {{
	opacity: 0.6;
}}

/* Close Button */
.close-button {{
	width: 1em;
	height: 1em;
	position: absolute;
	right: 1em;
	top: 1em;
	overflow: hidden;
	text-indent: 1em;
	font-size: 0.75em;
	border: none;
	background: transparent;
	color: transparent;
}}

.close-button::before,
.close-button::after {{
	content: '';
	position: absolute;
	width: 3px;
	height: 100%;
	top: 0;
	left: 50%;
	background: #bdc3c7;
}}

.close-button::before {{
	-webkit-transform: rotate(45deg);
	transform: rotate(45deg);
}}

.close-button::after {{
	-webkit-transform: rotate(-45deg);
	transform: rotate(-45deg);
}}

/* Menu */
.menu-wrap {{
    position: absolute;
    z-index: 1001;
    width: 380px;
    height: 100%;
    background: #373a47;
    padding: 2.5em 1.5em 0;
    font-size: 1.15em;
    -webkit-transform: translate3d(-380px,0,0);
    transform: translate3d(-380px,0,0);
    -webkit-transition: -webkit-transform 0.3s;
    transition: transform 0.3s;
    -webkit-transition-timing-function: cubic-bezier(0.7,0,0.3,1);
    transition-timing-function: cubic-bezier(0.7,0,0.3,1);
}}

.menu, 
.icon-list {{
	height: 100%;
}}

.icon-list {{
	-webkit-transform: translate3d(0,100%,0);
	transform: translate3d(0,100%,0);
}}

.icon-list a {{
	display: block;
	padding: 0.8em;
	-webkit-transform: translate3d(0,500px,0);
	transform: translate3d(0,500px,0);
}}

.icon-list,
.icon-list a {{
	-webkit-transition: -webkit-transform 0s 0.4s;
	transition: transform 0s 0.4s;
	-webkit-transition-timing-function: cubic-bezier(0.7,0,0.3,1);
	transition-timing-function: cubic-bezier(0.7,0,0.3,1);
}}

.icon-list a:nth-child(2) {{
	-webkit-transform: translate3d(0,1000px,0);
	transform: translate3d(0,1000px,0);
}}

.icon-list a:nth-child(3) {{
	-webkit-transform: translate3d(0,1500px,0);
	transform: translate3d(0,1500px,0);
}}

.icon-list a:nth-child(4) {{
	-webkit-transform: translate3d(0,2000px,0);
	transform: translate3d(0,2000px,0);
}}

.icon-list a:nth-child(5) {{
	-webkit-transform: translate3d(0,2500px,0);
	transform: translate3d(0,2500px,0);
}}

.icon-list a:nth-child(6) {{
	-webkit-transform: translate3d(0,3000px,0);
	transform: translate3d(0,3000px,0);
}}

.icon-list a span {{
	margin-left: 10px;
	font-weight: 700;
}}

/* Shown menu */
.show-menu .menu-wrap {{
	-webkit-transform: translate3d(0,0,0);
	transform: translate3d(0,0,0);
	-webkit-transition: -webkit-transform 0.6s;
	transition: transform 0.6s;
	-webkit-transition-timing-function: cubic-bezier(0.7,0,0.3,1);
	transition-timing-function: cubic-bezier(0.7,0,0.3,1);
}}

.show-menu .icon-list,
.show-menu .icon-list a {{
	-webkit-transform: translate3d(0,0,0);
	transform: translate3d(0,0,0);
	-webkit-transition: -webkit-transform 0.6s;
	transition: transform 0.6s;
	-webkit-transition-timing-function: cubic-bezier(0.7,0,0.3,1);
	transition-timing-function: cubic-bezier(0.7,0,0.3,1);
}}

.show-menu .icon-list a {{
	-webkit-transition-duration: 0.7s;
	transition-duration: 0.7s;
}}

.show-menu .content::before {{
	opacity: 1;
	-webkit-transition: opacity 0.6s;
	transition: opacity 0.6s;
	-webkit-transition-timing-function: cubic-bezier(0.7,0,0.3,1);
	transition-timing-function: cubic-bezier(0.7,0,0.3,1);
	-webkit-transform: translate3d(0,0,0);
	transform: translate3d(0,0,0);
}}
</style>
"""

template = header + normalize + icons + styles + body + scripts + footer



def render(subject, messages, attachments):
    if attachments:
        attachments = ["<a href=\""+f+"\"><i class='icon-download'></i>"+f+"</a>" for f in attachments]
        all_attachments_button = ("<a href='/attachments.tgz'>"
                                  "<i class='icon-file-archive'></i>"
                                  "All attachment <small>(.tgz)</small></a>")
    else:
        attachments = ""
        all_attachments_button = ""

    messages = "\n".join(messages)

    return template.format(
        subject=subject,
        attachments="\n".join(attachments),
        all_attachments_button=all_attachments_button,
        messages=messages,
    )
