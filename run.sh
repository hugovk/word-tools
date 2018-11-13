#!/bin/bash
set -e

for BOT in nixibot favibot lovihatibot
do
    python2 $BOT.py --tweet none --ini ~/bin/data/$BOT.ini --csv ~/bin/data/$BOT.csv
done
