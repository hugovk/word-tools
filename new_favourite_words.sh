CSV_FILE=/TODO/full/path/to/newfavouritewords.csv

grep ",is my new favourite word," $CSV_FILE > /tmp/new_favourite_words.tmp
grep ",is my new favorite word,"  $CSV_FILE > /tmp/new_favorite_words.tmp
grep ",is my new fave word,"      $CSV_FILE > /tmp/new_fave_words.tmp

# Slice out first column containing just the fav[o[u]ri]te word
cat /tmp/new_favourite_words.tmp | cut -d, -f1 > /tmp/new_favourite_words.lst
cat /tmp/new_favorite_words.tmp  | cut -d, -f1 > /tmp/new_favorite_words.lst
cat /tmp/new_fave_words.tmp      | cut -d, -f1 > /tmp/new_fave_words.lst
cat $CSV_FILE                    | cut -d, -f1 > /tmp/new_favourite_favorite_and_fave_words.lst

# Find top 10s
for f in favourite favorite fave favourite_favorite_and_fave
do
#     echo "new_${f}_words"
    most_frequent_words.py "/tmp/new_${f}_words.lst"
done

# Make word clouds (uses https://github.com/hugovk/word_cloud)

for f in favourite favorite fave favourite_favorite_and_fave
do
    echo "Create word cloud for 'is my new $f word'"
    python /TODO/full/path/to/word_cloud/wordcloud.py --stopwords None --width 800 --height 400 --fontfile "/Library/Fonts/Times New Roman.ttf" "/tmp/new_${f}_words.lst" -o "/tmp/new_${f}_words.png"
done
