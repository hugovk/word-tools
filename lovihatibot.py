#!/usr/bin/env python
"""
Find examples of "I love/hate the word X" on Twitter and
add them to Wordnik word lists.
"""
import word_tools

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing
except:
    pass

# Twitter: create an app at https://dev.twitter.com/apps/new
CONSUMER_KEY = "TODO_ENTER_YOURS_HERE"
CONSUMER_SECRET = "TODO_ENTER_YOURS_HERE"
OAUTH_TOKEN = "TODO_ENTER_YOURS_HERE"
OAUTH_SECRET = "TODO_ENTER_YOURS_HERE"

love_max_id, hate_max_id = 0, 0
STUFF = [
    ["I love the word", "I hate the word"],  # search term
    [love_max_id, hate_max_id],
    ["twitter-loves", "twitter-hates"]  # Wordnik word list permalink
    ]

# "I love the word X" or "X is my favourite new word"?
TARGET_WORD_FOLLOWS_SEARCH_TERM = True

# Test mode doesn't actually save csv, ini or update Wordnik or Twitter
TEST_MODE = False

if __name__ == '__main__':
    parser = word_tools.do_argparse('Find examples of "I love/hate the word X" on Twitter and add them to Wordnik word lists.')
    parser.add_argument(
        '-i', '--ini',
        default='/Users/hugo/Dropbox/bin/data/lovihatibot.ini',
        help='INI file location for storing last Twitter ID checked')
    parser.add_argument(
        '-c', '--csv',
        default='/Users/hugo/Dropbox/bin/data/lovihatibot.csv',
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

        tweet_prefix = STUFF[0][i].replace("I ", "Tweeters ")
        if "love" in STUFF[0][i]:
            tweet_prefix = u"\u2665 " + tweet_prefix  # heart
        else:
            tweet_prefix = u"\u2020 " + tweet_prefix  # dagger

        if args.tweet == "random":
            from random import choice
            # exclude none and random:
            args.tweet = choice(word_tools.TWEET_CHOICES[1:-1])
            print("Random tweet type:" + args.tweet)

        word_tools.tweet_those(
            words, tweet_prefix, args.csv, search_term, args.tweet)

        word_tools.save_ini(args.ini, STUFF)

# End of file
