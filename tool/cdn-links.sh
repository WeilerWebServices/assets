#!/bin/sh

# CDN Links for Assets

cd /Users/air/github/Projects/assets/

tree > /Users/air/github/Projects/assets/tool/remote-urls.md

/usr/local/bin/python3 /Users/air/bin/cdn-links.py >> /Users/air/github/Projects/assets/tool/remote-urls.md

open -a TextEdit /Users/air/github/Projects/assets/tool/remote-urls.md
