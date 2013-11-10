#!/usr/bin/env python
"""
Wordnik and Twitter utility functions
"""

################## GENERAL ##################

import ConfigParser
import csv
import re
import os

# Test mode doesn't actually save csv, ini or update Wordnik or Twitter
TEST_MODE = False

# Remove duplicates from a list but keep in order
# http://stackoverflow.com/questions/480214/
def dedupe(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print text.encode('utf-8')

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

def find_words(search_term, target_word_follows_search_term, results, csv_file):
    words = []
    statuses = []

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

    for status in results['statuses']:
        text = status['text']
        print "----"
        print_it(text)

        if text.startswith('RT'): # Ignore retweets
            continue
        if ' RT ' in text and text.find(' RT ') < text.find(search_term): # Ignore retweets
            continue
        if text[0] == u"\u201c": # ignore tweets beginning with a curly left double quote, they're often quoting another person's tweet
            continue
        if text.startswith('"@'): # ignore, probably quoting another's tweet (but don't ignore: '"word" is my new favourite')
            continue

        match = re.search(pattern, text)
        if match:
            word = match.group(1).lower()

            # Ignore some common words
            if word.lower() in ["it", "this", "that", "which", "and", "a", "of", "in", "but", "there"]:
                continue

            if len(word) == 0:
                continue

            # OK, got something
            print_it(">" + word + "<")
            # print_it(status['user']['screen_name'])
            words.append(word)
            statuses.append(status)

    update_csv(csv_file, search_term, words, statuses)
    return words

################## WORDNIK ##################

from wordnik import *

# Wordnik: get API key at http://developer.wordnik.com/
WORDNIK_API_KEY = "TODO_ENTER_YOURS_HERE"
WORDNIK_USERNAME = "TODO_ENTER_YOURS_HERE"
WORDNIK_PASSWORD = "TODO_ENTER_YOURS_HERE"
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

def tweet_those(words, tweet_prefix):
    if len(words) < 1: # validation
        return

    # Remove duplicates
    words = dedupe(words)

    tweet = tweet_prefix
    if len(words) == 1: # get the plural right
        tweet += ": "
    else:
        tweet += "s: "
    new_tweet = tweet

    words_remaining = list(words)
    for i, word in enumerate(words):
        if i == 0:
            new_tweet = tweet + word
        else:
            new_tweet = tweet + ", " + word
        if len(tweet) + len(word) > 140:
            break
        tweet = new_tweet
        words_remaining.pop(0)

    if len(tweet) + 1 <= 140: # Finish properly, if there's room
        tweet += "."

    print "TWEET THIS:", tweet

    if not TEST_MODE:
        try:
            t.statuses.update(status=tweet)
        except:
            pass

    if len(words_remaining) > 0:
        tweet_those(words_remaining, tweet_prefix)

# End of file
