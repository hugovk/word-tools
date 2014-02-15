#!/usr/bin/env python
"""
Wordnik and Twitter utility functions
"""

################## GENERAL ##################

import argparse
import ConfigParser
import csv
import re
import os
import time

# Test mode doesn't actually save csv, ini or update Wordnik or Twitter
TEST_MODE = False

TWEET_CHOICES=('none', 'latest', 'latest_onetweet', '24hours', '7days', '30days', 'alltime', 'random')

# Remove duplicates from a list but keep in order
# http://stackoverflow.com/questions/480214/
def dedupe(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print text.encode('utf-8')

def do_argparse(description=None):
    parser = argparse.ArgumentParser(description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tweet', default='latest', choices=TWEET_CHOICES,
        help="How to tweet the results.")
    return parser

# The `stuff` list looks like:
#     [
#     ["I love the word", "I hate the word"], # search term
#     [love_max_id, hate_max_id],
#     ["twitter-loves", "twitter-hates"] # Wordnik word list permalink
#     ]

def load_ini(ini_file, stuff):
    config = ConfigParser.ConfigParser()
    result = config.read(ini_file)
    if result:
        # print summary
        for i in range(len(stuff[1])):
            # Load max IDs using permalink as key
            stuff[1][i] = config.get("max_ids", stuff[2][i])
    return stuff

    print "Loaded:", stuff[1]

def save_ini(ini_file, stuff):
    print "Save:", stuff[1]

    config = ConfigParser.ConfigParser()
    config.add_section("max_ids")
    for i in range(len(stuff[1])):
        # Save max IDs using permalink as key
        config.set("max_ids", stuff[2][i], stuff[1][i])
    
    if TEST_MODE:
        return
    with open(ini_file, 'wb') as configfile:
        config.write(configfile)

def update_csv(csv_file, search_term, words, statuses):
    file_exists = os.path.exists(csv_file)
    if TEST_MODE:
        return
    fd = open(csv_file, 'ab')
    try:
        writer = csv.writer(fd)
        if not file_exists: # add header
            writer.writerow( ('word', 'search_term', 'created_at', 'id_str', 'screen_name', 'user_name', 'text') )
        for i,status in enumerate(statuses):
            csv_data = [words[i], search_term, status['created_at'], status['id_str'], status['user']['screen_name'], status['user']['name'], status['text'].replace('\n', ' ')]
            for i,field in enumerate(csv_data):
                csv_data[i] = field.encode('utf8')
            writer.writerow(csv_data)

    finally:
        fd.close()

def get_pattern(search_term, target_word_follows_search_term):
    # word boundary,one or more word chars, any '-*, one or more word chars, word boundary
    word_pattern = "[^\w]*(\w+(['-\*]*\w)*)[^\w]*"
    
    if target_word_follows_search_term:
    # Matches search term ("I love the word") followed by whitespace then at least one
    # [whitespace, period, exclamation mark, comma, brackets, question mark]
#         pattern = re.compile(search_term + "\s+([^\s.!,()?]+)", re.IGNORECASE)

        # \s = whitespace
        # \w = word characters (a-zA-Z0-9_) but re.UNICODE allows umlauts and things
        # search term, whitespace, then any number of non-word chars,
        # then begin group: one or more word chars, then any number of apostrophes and 
        # hyphens as long as they are followed by a word char. 
        # Then end the group with any number of non-word chars.
        pattern = re.compile(search_term + "\s+" + word_pattern,
            re.IGNORECASE | re.UNICODE)
    else:
    # Matches at least something that's NOT [whitespace, period, exclamation mark, comma, 
    # open bracket, close bracket], followed by at least one [whitespace, period, 
    # exclamation mark, comma] and then "is my new etc."
        pattern = re.compile(word_pattern + "\s+" + search_term,
            re.IGNORECASE | re.UNICODE)
    
    return pattern

def word_from_text(text, pattern, search_term):
    """ If matching word found in tweet text, return it. Else return None """
    print_it(text)

    if text.startswith('RT'): # Ignore retweets
        return None
    if ' RT ' in text and text.find(' RT ') < text.find(search_term): # Ignore retweets
        return None
    if text[0] == u"\u201c": # ignore tweets beginning with a curly left double quote, they're often quoting another person's tweet
        return None
    if text.startswith('"@'): # ignore, probably quoting another's tweet (but don't ignore: '"word" is my new favourite')
        return None

    match = re.search(pattern, text)
    if match:
        word = match.group(1).lower()

        # Ignore some common words
        if word.lower() in ["it", "this", "that", "which", "and", "a", "of", "in", "but", "there"]:
            return None

        if len(word) == 0:
            return None

        # OK, got something
        print_it(">" + word + "<")
        return word

    # Nothing found
    return None

def extract_words(search_term, target_word_follows_search_term, results):
    words = []
    statuses = []
    pattern = get_pattern(search_term, target_word_follows_search_term)

    for status in results['statuses']:
        text = status['text']
        print "----"
        word = word_from_text(text, pattern, search_term)
        if word is not None:
            # print_it(status['user']['screen_name'])
            words.append(word)
            statuses.append(status)

    return words, statuses

def find_words(search_term, target_word_follows_search_term, results, csv_file):
    words, statuses = extract_words(search_term, target_word_follows_search_term, results)
    update_csv(csv_file, search_term, words, statuses)
    return words

def find_colnum(heading, row):
    """Find the coloumn number for a given heading"""
    # Find word column
    found_colnum = None
    for colnum, col in enumerate(row):
        if heading == col:
            found_colnum = colnum
            break
    return found_colnum

def load_words_from_csv(csv_file, search_term, seconds_delta = None):
    """Load the CSV and return the top words for a given time period"""
    cutoff = 0
    if seconds_delta:
        epoch_time = int(time.time())
        cutoff = epoch_time - seconds_delta

    word_colnum, searchterm_colnum, created_at_colnum = None, None, None
    matched_words = []
    ifile  = open(csv_file, "rb")
    reader = csv.reader(ifile)

    for rownum, row in enumerate(reader):
        # Save header row
        if rownum == 0:
            header = row

            # Find columns
            word_colnum = find_colnum("word", row)
            searchterm_colnum = find_colnum("search_term", row)
            created_at_colnum = find_colnum("created_at", row)
            text_colnum = find_colnum("text", row)

        else: # not header
            # Kill the spambot!
            if row[searchterm_colnum] != search_term:
                continue
            text = row[text_colnum]
            if text[0] == "@" and "I love the word douchebag. http://t.co/" in text:
#                 print row[text_colnum]
                continue

            # seconds since epoch:
            timestamp = time.mktime(time.strptime(row[created_at_colnum],'%a %b %d %H:%M:%S +0000 %Y'))
            if timestamp > cutoff:
                matched_words.append(row[word_colnum])

    ifile.close()

    import most_frequent_words
    # Max tweet length is 140
    # Let's naively set an upper limit of 140/3: one-character word, comma and space
    top_words = most_frequent_words.most_frequent_words(matched_words, 140/3)
    return top_words

################## WORDNIK ##################

from wordnik import *

# Wordnik: get API key at http://developer.wordnik.com/
WORDNIK_API_KEY = "3fd3445662c1ac873962d06094f057f39d4711730e1adc28f"
WORDNIK_USERNAME = "hugovk"
WORDNIK_PASSWORD = "mytopsecretwordnikpassword"
WORDNIK_TOKEN = None

wordnik_client = swagger.ApiClient(WORDNIK_API_KEY, 'http://api.wordnik.com/v4')
wordListApi = WordListApi.WordListApi(wordnik_client)

# TODO: Save token to ini file
def get_wordnik_token():
    import getpass
    if WORDNIK_USERNAME:
        my_username = WORDNIK_USERNAME
    else:
        my_username = raw_input("Enter your Wordnik username: ")
    if WORDNIK_PASSWORD:
        my_password = WORDNIK_PASSWORD
    else:
        my_password = getpass.getpass("Enter your Wordnik password: ")

    accountApi = AccountApi.AccountApi(wordnik_client)
    result = accountApi.authenticate(my_username, my_password)
    token = result.token
    print "Your Wordnik token is:", token
    return token

def add_to_wordnik(words, wordlist_permalink):
    if len(words) == 0:
        return

    if TEST_MODE:
        return

    global WORDNIK_TOKEN
    if WORDNIK_TOKEN is None:
    # Only need to do this once
        WORDNIK_TOKEN = get_wordnik_token()

    words.sort()
    print_it("Words: " + ', '.join(words))
    if len(words) == 1:
        number = "1 word"
    else:
        number = str(len(words)) + " words"
    print "Adding " + number + " to Wordnik list:", wordlist_permalink

    from wordnik.models import StringValue
    words_to_add = []
    for word in words:
        word_to_add = StringValue.StringValue()
        word_to_add.word = word
        words_to_add.append(word_to_add)

    print  wordlist_permalink, WORDNIK_TOKEN, words

    result = wordListApi.addWordsToWordList(wordlist_permalink, WORDNIK_TOKEN, body=words_to_add)
    
    print len(words), "words added"


################## TWITTER ##################

from twitter import * # https://github.com/sixohsix/twitter

t = None

def init_twitter(oauth_token, oauth_secret,
                           consumer_key, consumer_secret):
    global t
    t = Twitter(auth=OAuth(oauth_token, oauth_secret,
                           consumer_key, consumer_secret))

def get_words_from_twitter(search_term, since_id=0):
    results = t.search.tweets(q='"' + search_term + '"', count=100, since_id=int(since_id))
    
    print results['search_metadata']
    print "Requested:\t", results['search_metadata']['count']
    print "Found:\t", len(results['statuses'])
    max_id = results['search_metadata']['max_id']
    print "Max ID:\t", max_id

    return max_id, results

def tweet_string(string):
    if len(string) <= 0:
        return
    if len(string) + 1 <= 140: # Finish properly, if there's room
        string += "."

    print "TWEET THIS:", string

    if not TEST_MODE:
        try:
            t.statuses.update(status=string)
        except Exception, e:
            print str(e)

def tweet_those(words, tweet_prefix, csv_file = None, search_term = None, mode = "latest"):
    # Remove duplicates
    words = dedupe(words)

    shuffle, tweet_all_words = False, False
    extra_prefix = ""
    if mode == "none" or TEST_MODE:
        return
    elif mode == "latest":
        tweet_all_words = True
    elif mode == "latest_onetweet":
        shuffle = True
    elif mode == "24hours":
        words = load_words_from_csv(csv_file, search_term, 24 * 60 * 60 * 60)
        extra_prefix += " (24 hours)"
    elif mode == "7days":
        words = load_words_from_csv(csv_file, search_term, 7 * 24 * 60 * 60 * 60)
        extra_prefix += " (7 days)"
    elif mode == "30days":
        words = load_words_from_csv(csv_file, search_term, 30 * 24 * 60 * 60 * 60)
        extra_prefix += " (30 days)"
    elif mode == "alltime":
        words = load_words_from_csv(csv_file, search_term, None)
        extra_prefix += " (all time)"
    else:
        print "Unknown mode:", mode
        return

    if len(words) < 1: # validation
        return

    if shuffle:
        from random import shuffle
        shuffle(words)

    tweet = tweet_prefix
    if len(words) == 1: # get the plural right
        tweet += extra_prefix + ": "
    else:
        tweet += "s" + extra_prefix + ": "
    new_tweet = tweet

    words_remaining = list(words)
    for i, word in enumerate(words):
        if i == 0:
            new_tweet = tweet + word
        else:
#             new_tweet = tweet + ", " + word
            new_tweet = tweet + " " + word
        if len(new_tweet) > 140:
            break
        else:
            tweet = new_tweet
        words_remaining.pop(0)

    tweet_string(tweet)

    if tweet_all_words and len(words_remaining) > 0:
        tweet_those(words_remaining, tweet_prefix)

# End of file
