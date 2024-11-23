#!/bin/sh

# CDN Links for Assets

cd ~/github/wws/assets/

touch ~/github/wws/assets/remote-urls.txt

tree > ~/github/wws/assets/remote-urls.txt

echo '\n\n###\n\n' >> ~/github/wws/assets/remote-urls.txt

/usr/local/bin/python3 ~/bin/python/cdn-assets-links.py >> ~/github/wws/assets/remote-urls.txt

open -a TextEdit ~/github/wws/assets/remote-urls.txt
