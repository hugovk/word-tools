#!/bin/bash
set -e

cd ~/github/word-tools/
./update.sh

python2 favibot.py --tweet retweet --ini ~/bin/data/favibot.ini --csv ~/bin/data/favibot.csv
