#!/usr/bin/env python
"""
Find examples of "X is my new favourite/favorite/fave" on Twitter and add them to Wordnik word lists.
"""
import ConfigParser
import csv
import os
import re
import string
import sys

from twitter import *
from wordnik import *

import timing

# Twitter: create an app at https://dev.twitter.com/apps/new
CONSUMER_KEY = "TODO_ENTER_YOURS_HERE"
CONSUMER_SECRET = "TODO_ENTER_YOURS_HERE"
OAUTH_TOKEN = "TODO_ENTER_YOURS_HERE"
OAUTH_SECRET = "TODO_ENTER_YOURS_HERE"

# Wordnik: get API key at http://developer.wordnik.com/
WORDNIK_API_KEY = "TODO_ENTER_YOURS_HERE"
WORDNIK_USERNAME = "TODO_ENTER_YOURS_HERE"
WORDNIK_PASSWORD = "TODO_ENTER_YOURS_HERE"
WORDNIK_TOKEN = None

INI_FILE = "/TODO/full/path/to/newfavouritewords.ini"
CSV_FILE = "/TODO/full/path/to/newfavouritewords.csv"

# Test mode doesn't actually save csv, ini or update Wordnik
TEST_MODE = False

# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print text.encode('utf-8')

def load_ini():
    favourite_max_id = 0
    favorite_max_id = 0
    fave_max_id = 0

    config = ConfigParser.ConfigParser()
    result = config.read(INI_FILE)
    if result:
        # print summary
        favourite_max_id = config.get("max_ids", "favourite")
        favorite_max_id = config.get("max_ids", "favorite")
        fave_max_id = config.get("max_ids", "fave")

    print "Loaded:", favourite_max_id, favorite_max_id, fave_max_id
    return favourite_max_id, favorite_max_id, fave_max_id

def save_ini(favourite_max_id, favorite_max_id, fave_max_id):
    print "Save:", favourite_max_id, favorite_max_id, fave_max_id

    config = ConfigParser.ConfigParser()
    config.add_section("max_ids")
    config.set("max_ids", "favourite", favourite_max_id)
    config.set("max_ids", "favorite", favorite_max_id)
    config.set("max_ids", "fave", fave_max_id)

    if TEST_MODE:
        return
    with open(INI_FILE, 'wb') as configfile:
        config.write(configfile)

def update_csv(search_term, words, statuses):
    if TEST_MODE:
        return
    file_exists = os.path.exists(CSV_FILE)
    fd = open(CSV_FILE, 'ab')
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
    print "Adding to Wordnik list:", wordlist_permalink



    from wordnik.models import StringValue
    words_to_add = []
    for word in words:
        word_to_add = StringValue.StringValue()
        word_to_add.word = word
        words_to_add.append(word_to_add)

    print  wordlist_permalink, WORDNIK_TOKEN, words

    result = wordListApi.addWordsToWordList(wordlist_permalink, WORDNIK_TOKEN, body=words_to_add)
    
    print len(words), "words added"

def get_words_from_twitter(search_term, since_id=0):
    words = []
    statuses = []

    results = t.search.tweets(q='"' + search_term + '"', count=100, since_id=int(since_id))
    print results['search_metadata']
    print "Requested:\t", results['search_metadata']['count']
    print "Found:\t", len(results['statuses'])
    max_id = results['search_metadata']['max_id']
    print "Max ID:\t", max_id

    # Matches at least something that's NOT [whitespace, period, exclamation mark, comma, 
    # open bracket, close bracket], followed by at least one [whitespace, period, 
    # exclamation mark, comma] and then "is my new etc."
    pattern = re.compile("([^\s.!,()]+)[\s.!,]+" + search_term, re.IGNORECASE)
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
            # Strip (balanced) enclosing quotes:
            if (word.startswith('"') and word.endswith('"')) or \
               (word.startswith("'") and word.endswith("'")):
                word = word[1:-1]
            # But ignore sole end quotes, it's probably the last word of a phrase, e.g. "Terra Flops"
            if word.endswith('"') or word.endswith("'"):
                continue
            # Strip hashtag hashes:
            if word.startswith('#'):
                word = word[1:]
            # Ignore some common words
            if word.lower() in ["it", "this", "that", "which"]:
                continue
            if len(word) == 0:
                continue

            # OK, got something
            print_it(">" + word + "<")
            # print_it(status['user']['screen_name'])
            words.append(word)
            statuses.append(status)

    update_csv(search_term, words, statuses)
    return max_id, words

if __name__ == '__main__':
    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET))
    wordnik_client = swagger.ApiClient(WORDNIK_API_KEY, 'http://api.wordnik.com/v4')

    wordListApi = WordListApi.WordListApi(wordnik_client)
    favourite_max_id, favorite_max_id, fave_max_id = load_ini()
    # favourite_max_id, favorite_max_id, fave_max_id = 0,0,0 # testing

    stuff = [
        ["is my new favourite word", "is my new favorite word", "is my new fave word"], # search term
        [favourite_max_id, favorite_max_id, fave_max_id],
        ["twitter-favourites", "twitter-favorites", "twitter-faves", ] # Wordnik word list permalink
        ]

    for i,search_term in enumerate(stuff[0]):
        stuff[1][i], words = get_words_from_twitter(search_term, stuff[1][i])
        add_to_wordnik(words, stuff[2][i])
        save_ini(stuff[1][0], stuff[1][1], stuff[1][2])

# End of file
