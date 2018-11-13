#!/bin/bash
set -e

cd ~/github/word-tools/
./update.sh

python2 lovihatibot.py --tweet retweet --ini ~/bin/data/lovihatibot.ini --csv ~/bin/data/lovihatibot.csv
