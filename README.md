muttd
=====
muttd is a standalone plugin for [mutt](http://www.mutt.org/) designed to improve readability and access to a mail and its attachments. It is based on 3 interoperating components:
* an extractor, treating each part of a MIME mail and writing them to the disk
* a renderer, creating a page formated with extracted results
* a minimal HTTP daemon, serving the page and attachments localy

## Requirements
* python 3.4: https://www.python.org/

## Features
* Preview any "text/*" based MIME message from your HTTP browser
  * Display inline attachments
* Sidebar
  * Download each attachment individually
  * Download a tarball containing all attachments
  * Download the original source file

## Installation
1. Extract the project archive wherever you want on the disk.

        $ cd ~/.mutt && wget https://github.com/debsquad/muttd/archive/master.zip 
        $ unzip master.zip && rm master.zip

2. Edit `muttd.py` and modify configuration variables to fit your needs, especially `DIR` which represents the working path used by both the daemon and extractor. Don't forget to create the folder on the disk if needed.

    ```py
    HOST = "127.0.0.1"                                                          
    PORT_NUMBER = 8090                                                          
    DIR = os.path.expanduser("~/.muttd/message")
    ```
3. Edit your `~/.muttrc` and define new maccros for muttd. _p_ will pipe current message and process its output using `extractmail.py`.

        macro pager p "<enter-command>unset wait_key<enter><pipe-entry>cat | ~/.mutt/muttd/extractmail.py -d ~/.muttd/message<enter>"
        macro index p "<enter-command>unset wait_key<enter><pipe-entry>cat | ~/.mutt/muttd/extractmail.py -d ~/.muttd/message<enter>"

## Usage
Start the daemon: 
```
$ cd ~/.mutt/muttd && ./muttd.py
```
Run `mutt` and press the previously defined maccro on any index entry or pager.

Entry is instantly available on your web browser: 
```
$ firefox http://localhost:8090/
```
## Authors
* Bertrand Janin [website](http://tamentis.com/)
* Vincent Tantardini [website](http://www.vtcreative.fr/)
