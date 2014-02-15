CSV_FILE=~/Dropbox/bin/data/favibot.csv

DEDUPE=/tmp/favibot.csv
rm $DEDUPE
awk '!a[$0]++' $CSV_FILE > $DEDUPE

rm /tmp/new_fa*.tmp
grep -i ",is my new favourite word," $DEDUPE > /tmp/new_favourite_words.tmp
grep -i ",is my new favorite word,"  $DEDUPE > /tmp/new_favorite_words.tmp
grep -i ",is my new fave word,"      $DEDUPE > /tmp/new_fave_words.tmp

# Slice out first column containing just the fav[o[u]ri]te word
rm /tmp/new_fa*.lst
cat /tmp/new_favourite_words.tmp | cut -d, -f1 > /tmp/new_favourite_words.lst
cat /tmp/new_favorite_words.tmp  | cut -d, -f1 > /tmp/new_favorite_words.lst
cat /tmp/new_fave_words.tmp      | cut -d, -f1 > /tmp/new_fave_words.lst
cat $DEDUPE                      | cut -d, -f1 > /tmp/new_favourite_favorite_and_fave_words.lst

# Find top 10s
for f in favourite favorite fave favourite_favorite_and_fave
do
#     echo "new_${f}_words"
    most_frequent_words.py "/tmp/new_${f}_words.lst"
done

# Make word clouds (uses https://github.com/hugovk/word_cloud)

rm /tmp/new_fa*.png
for f in favourite favorite fave favourite_favorite_and_fave
do
    echo "Create word cloud for 'is my new $f word'"
    python ~/Dropbox/bin/word_cloud/wordcloud.py --stopwords None --width 1024 --height 576 --fontfile "/Library/Fonts/Times New Roman.ttf" "/tmp/new_${f}_words.lst" -o "/tmp/new_${f}_words.png"
done

echo "Done."
