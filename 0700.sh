#!/bin/bash
set -e

cd ~/github/word-tools/
./update.sh

for BOT in nixibot favibot lovihatibot
do
    python2 $BOT.py --tweet random --ini ~/bin/data/$BOT.ini --csv ~/bin/data/$BOT.csv
done
