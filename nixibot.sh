CSV_FILE=~/Dropbox/bin/data/nixibot.csv

DEDUPE=/tmp/nixibot.csv
rm $DEDUPE
awk '!a[$0]++' $CSV_FILE > $DEDUPE

rm /tmp/*i*n*t_words.tmp
grep -i ",ain't a word,"  $DEDUPE > /tmp/aint_words.tmp
grep -i ",isn't a word,"  $DEDUPE > /tmp/isnt_words.tmp
grep -i ",is not a word," $DEDUPE > /tmp/is_not_words.tmp

# Slice out first column containing just the fav[o[u]ri]te word
rm /tmp/*i*n*t_words.lst
cat /tmp/aint_words.tmp   | cut -d, -f1 > /tmp/aint_words.lst
cat /tmp/isnt_words.tmp   | cut -d, -f1 > /tmp/isnt_words.lst
cat /tmp/is_not_words.tmp | cut -d, -f1 > /tmp/is_not_words.lst
cat $DEDUPE               | cut -d, -f1 > /tmp/aint_isnt_and_isnot_words.lst

# Find top 10s
for f in aint isnt is_not aint_isnt_and_isnot
do
    most_frequent_words.py "/tmp/${f}_words.lst"
done

# Make word clouds (uses https://github.com/hugovk/word_cloud)

rm /tmp/*i*n*t_words.png
for f in aint isnt is_not aint_isnt_and_isnot
do
    echo "Create word cloud for '$f a word'"
    python ~/Dropbox/bin/word_cloud/wordcloud.py --stopwords None --width 1024 --height 576 --fontfile "/Library/Fonts/Times New Roman.ttf" "/tmp/${f}_words.lst" -o "/tmp/${f}_words.png"
done

echo "Done."
