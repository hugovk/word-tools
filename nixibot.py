#!/usr/bin/env python
"""
Find examples of "X is not/isn't/ain't a word" on Twitter and
add them to Wordnik word lists.
"""
import word_tools

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing
    assert timing  # silence warnings
except ImportError:
    pass

# Twitter: create an app at https://dev.twitter.com/apps/new
CONSUMER_KEY = "TODO_ENTER_YOURS_HERE"
CONSUMER_SECRET = "TODO_ENTER_YOURS_HERE"
OAUTH_TOKEN = "TODO_ENTER_YOURS_HERE"
OAUTH_SECRET = "TODO_ENTER_YOURS_HERE"

isnot_max_id, isnt_max_id, aint_max_id = 0, 0, 0
STUFF = [
    ["ain't a word", "isn't a word", "is not a word"],  # search term
    [aint_max_id, isnt_max_id, isnot_max_id],
    ["twitter-aints", "twitter-isnts", "twitter-isnots", ]  # Wordnik word list permalink
    ]

# e.g. "I love the word X" (True) or "X is my favourite new word" (False)?
TARGET_WORD_FOLLOWS_SEARCH_TERM = False

# Test mode doesn't actually save csv, ini or update Wordnik
TEST_MODE = True

if __name__ == '__main__':
    # args = word_tools.do_argparse()
    parser = word_tools.do_argparse("Find examples of \"X is not/isn't/ain't a word\" on Twitter and add them to Wordnik word lists.")
    parser.add_argument(
        '-i', '--ini',
        default='/Users/hugo/Dropbox/bin/data/nixibot.ini',
        help='INI file location for storing last Twitter ID checked')
    parser.add_argument(
        '-c', '--csv',
        default='/Users/hugo/Dropbox/bin/data/nixibot.csv',
        help='CSV file location for storing matching tweets')
    args = parser.parse_args()

    word_tools.init_twitter(
        OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    STUFF = word_tools.load_ini(args.ini, STUFF)  # updates STUFF[1]

    for i, search_term in enumerate(STUFF[0]):
        STUFF[1][i], results = word_tools.get_words_from_twitter(
            search_term, STUFF[1][i])
        words = word_tools.find_words(
            search_term, TARGET_WORD_FOLLOWS_SEARCH_TERM, results, args.csv)

        if not TEST_MODE:
            word_tools.add_to_wordnik(words, STUFF[2][i])

        tweet_prefix = STUFF[0][i]
        tweet_prefix = u"\u2260 " + tweet_prefix # not equal to

        if args.tweet == "random":
            from random import choice
            # exclude none and random:
            args.tweet = choice(word_tools.TWEET_CHOICES[1:-1])
            print("Random tweet type:" + args.tweet)

        word_tools.tweet_those(
            words, tweet_prefix, args.csv, search_term, args.tweet)

        word_tools.save_ini(args.ini, STUFF)

# End of file
