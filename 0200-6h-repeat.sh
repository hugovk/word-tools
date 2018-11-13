#!/bin/bash
set -e

cd ~/github/word-tools/
./update.sh

python2 nixibot.py --tweet retweet --ini ~/bin/data/nixibot.ini --csv ~/bin/data/nixibot.csv
