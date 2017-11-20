muttd
=====
muttd is a Python-based plugin for mutt (http://www.mutt.org/) designed to
improve readability and access to a mail and its attachments (locally and
remotely via SSH) through a browser. It is based on 2 commands:

- ``muttd extract`` - called from mutt, it extract each part of a MIME mail and
  write them to disk
- ``muttd serve`` - long running process which serve that email via HTTP, with
  all its attachments

Requirements
------------
- python 2.7+ or 3.4+: https://www.python.org/
- six

Features
--------
- Preview any ``text/*`` based MIME message from your HTTP browser

  * Display inline attachments

- Sidebar

  * Download each attachment individually
  * Download a tarball containing all attachments
  * Download the original source file (open it in Mail.app, Outlook, etc.)

Installation
------------
1. Install via your OS' packaging system or pip::

      $ pip install muttd
   
2. Edit your ``~/.muttrc`` and define new macros for muttd. ``A`` will pipe
current message and process its output using ``extractmail.py``::

       macro pager A "<enter-command>unset wait_key<enter><pipe-entry>muttd extract<enter>"
       macro index A "<enter-command>unset wait_key<enter><pipe-entry>muttd extract<enter>"

3. Run ``muttd server`` in a tmux/screen tab (or supervisord running as your
   user if you really must).

Configuration
-------------
By default, muttd will run on 127.0.0.1 port 8090, you can override that using
the ``~/.muttd/config`` file.  Here is an example configuration::

    [general]
    # Where muttd extract saves the message and where server reads it.
    message_path = ~/.muttd/message

    [server]
    address = "127.0.0.1"                                                          
    port = 8090                                                          

Usage
-----
Assuming the muttd server is running and you have used the above mutt macro,
you can then:

1. Highlight a message or open a message in mutt and type ``A``.
2. Open your browser on http://localhost:8090/

Remote usage
------------
If you run mutt on a server, you will want to download attachment and render
HTML emails without having to move them around.  It's easy to create a port
forwarding with SSH as you connect to your server to make that seamless.  Add
the following to your ``~/.ssh/config``::

    Host your_server
        LocalForward 127.0.0.1:8090 127.0.0.1:8090

The workflow remains the same, however you can now open that email from your
laptop/workstation.

Authors
-------
* Bertrand Janin (http://tamentis.com/)
* Vincent Tantardini (http://www.vtcreative.fr/)
