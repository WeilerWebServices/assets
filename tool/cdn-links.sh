#!/bin/sh

# CDN Links for Assets

cd /Users/air/github/Projects/assets/

tree > /Users/air/github/Projects/assets/tool/py/remote-urls.txt

/usr/local/bin/python3 /Users/air/github/Projects/assets/tool/py/cdn-links.py > /Users/air/github/Projects/assets/tool/py/remote-urls.txt

open -a TextEdit /Users/air/github/Projects/assets/tool/py/remote-urls.txt

cd -
