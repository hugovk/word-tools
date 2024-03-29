word-tools
==========

[![Build Status](https://travis-ci.org/hugovk/word-tools.svg?branch=master)](https://travis-ci.org/hugovk/word-tools)
[![Coverage Status](https://coveralls.io/repos/github/hugovk/word-tools/badge.svg?branch=master)](https://coveralls.io/github/hugovk/word-tools?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/hugovk/word-tools/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/hugovk/word-tools/?branch=master)
[![Code Health](https://landscape.io/github/hugovk/word-tools/master/landscape.png)](https://landscape.io/github/hugovk/word-tools/master)
[![Python: 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tools to do things with words

favibot
-------

`favibot.py` searches Twitter for tweets containing "[X] is my new favourite word". It then takes all those new favourite words, logs them, lowercases them, and adds them to a [list of words on Wordnik](http://www.wordnik.com/lists/twitter-favourites). It then [tweets them](https://twitter.com/favibot) and `favibot.sh` runs on the logged words and makes top 10 lists and [word clouds](http://www.flickr.com/photos/hugovk/sets/72157636928894765/).

It also does the same for "[X] is my new favorite word" and "[X] is my new fave word" so you can see some geographic variation.

The word lists on Wordnik:
 * http://www.wordnik.com/lists/twitter-favourites
 * http://www.wordnik.com/lists/twitter-favorites
 * http://www.wordnik.com/lists/twitter-faves

Follow along:
 * https://twitter.com/favibot

Word clouds from the first six months:
 * http://www.flickr.com/photos/hugovk/sets/72157636928894765/

Inspired by:
 * http://www.wordnik.com/lists/outcasts


[More info here.](http://laivakoira.typepad.com/blog/2013/10/twitters-new-favourite-words.html)

lovihatibot
-----------

This is similar to favibot, but for "I love the word [X]" and "I hate the word [X]".

The word lists on Wordnik:
 * http://www.wordnik.com/lists/twitter-loves
 * http://www.wordnik.com/lists/twitter-hates

Follow along:
 * https://twitter.com/lovihatibot

Word clouds from the first month:
 * https://secure.flickr.com/photos/hugovk/11114253096/
 * https://secure.flickr.com/photos/hugovk/11114260534/

nixibot
-------

Similar again, but for "[X] is not a word", "[X] isn't a word" and "[X] ain't a word".

The word lists on Wordnik:
 * http://www.wordnik.com/lists/twitter-isnots
 * http://www.wordnik.com/lists/twitter-isnts
 * http://www.wordnik.com/lists/twitter-aints

Follow along:
 * https://twitter.com/nixibot

See also:
 * https://twitter.com/nixicon

(Not yet word clouded.)

