muttd
=====
muttd is a mail previewer for Mutt designed to improve readability and access to HTML mails and/or attachments. It is based on 3 interoperating components:
* an extractor, treating each part of a MIME mail and writing them to the disk
* a renderer, generating a page displaying the extracted results
* a minimal HTTP daemon, serving generated results localy

## Requirements
* python 3.4: https://www.python.org/

## Installation
1. Extract the project archive wherever you want on the disk.

        $ cd ~/.mutt && wget https://github.com/debsquad/muttd/archive/master.zip 
        $ unzip master.zip && rm master.zip

2. Edit _muttd.py_ and modify configuration variables to fit your needs, especially _DIR_ which represents the working path used by both the daemon and extractor. Don't forget to create the folder on the disk if needed.

        HOST = "127.0.0.1"                                                          
        PORT_NUMBER = 8090                                                          
        DIR = os.path.expanduser("~/.muttd/message")

3. Edit your _~/.muttrc_ and define new maccros for muttd. Defined shortcut (_p_) will pipe current message and process its output using _extractmail.py_.

        macro pager p "<enter-command>unset wait_key<enter><pipe-entry>cat | ~/.mutt/muttd/extractmail.py -d ~/.muttd/message<enter>"
        macro index p "<enter-command>unset wait_key<enter><pipe-entry>cat | ~/.mutt/muttd/extractmail.py -d ~/.muttd/message<enter>"

## Usage
Start the daemon: 
```
$ ~/.mutt/muttd/muttd
```
Run mutt and press the previously defined maccro on any index entry or pager.

Entry is instantly available on your web browser: 
```
$ firefox http://localhost:8090/
```
## Notes

## Authors
