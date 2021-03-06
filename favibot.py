#!/usr/bin/env python
"""
Find examples of "X is my new favourite/favorite/fave" on Twitter and
add them to Wordnik word lists.
"""
import word_tools
from favibot_secrets import CONSUMER_KEY, CONSUMER_SECRET, OAUTH_SECRET, OAUTH_TOKEN

# Optional, http://stackoverflow.com/a/1557906/724176
try:
    import timing

    assert timing  # silence warnings
except ImportError:
    pass

favourite_max_id, favorite_max_id, fave_max_id = 0, 0, 0
STUFF = [
    # search term:
    ["is my new fave word", "is my new favorite word", "is my new favourite word"],
    [fave_max_id, favorite_max_id, favourite_max_id],
    # Wordnik word list permalink:
    ["twitter-faves", "twitter-favorites", "twitter-favourites"],
]

# e.g. "I love the word X" (True) or "X is my favourite new word" (False)?
TARGET_WORD_FOLLOWS_SEARCH_TERM = False

if __name__ == "__main__":
    # args = word_tools.do_argparse()
    parser = word_tools.do_argparse(
        'Find examples of "X is my new favourite/favorite/fave" on Twitter '
        "and add them to Wordnik word lists."
    )
    parser.add_argument(
        "-i",
        "--ini",
        default="/Users/hugo/Dropbox/bin/data/favibot.ini",
        help="INI file location for storing last Twitter ID checked",
    )
    parser.add_argument(
        "-c",
        "--csv",
        default="/Users/hugo/Dropbox/bin/data/favibot.csv",
        help="CSV file location for storing matching tweets",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Don't save CSV, INI or update Wordnik",
    )
    args = parser.parse_args()

    word_tools.TEST_MODE = args.dry_run

    word_tools.init_twitter(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    STUFF = word_tools.load_ini(args.ini, STUFF)  # updates STUFF[1]

    for i, search_term in enumerate(STUFF[0]):
        STUFF[1][i], results = word_tools.get_words_from_twitter(
            search_term, STUFF[1][i]
        )
        words = word_tools.find_words(
            search_term, TARGET_WORD_FOLLOWS_SEARCH_TERM, results, args.csv
        )

        if not args.dry_run:
            word_tools.add_to_wordnik(words, STUFF[2][i])

        tweet_prefix = STUFF[0][i].replace("is my ", "Twitter's ")
        tweet_prefix = "\u2605 " + tweet_prefix  # heart

        if args.tweet == "random":
            from random import choice

            # exclude none and random:
            args.tweet = choice(word_tools.TWEET_CHOICES[1:-2])
            print("Random tweet type:" + args.tweet)

        word_tools.tweet_those(words, tweet_prefix, args.csv, search_term, args.tweet)

        word_tools.save_ini(args.ini, STUFF)

# End of file
