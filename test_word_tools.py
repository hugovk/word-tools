#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for word_tools.py
"""
import unittest
import word_tools


class TestFindWords(unittest.TestCase):

    def setUp(self):
        self.setup_i_hate_the_word()

    def setup_i_hate_the_word(self):
        self.search_term = "I hate the word"
        self.target_word_follows_search_term = True
        self.pattern = word_tools.get_pattern(
            self.search_term,
            self.target_word_follows_search_term)

    def setup_aint_a_word(self):
        self.search_term = "ain't a word"
        self.target_word_follows_search_term = False
        self.pattern = word_tools.get_pattern(
            self.search_term,
            self.target_word_follows_search_term)

    def test_word1(self):
        text = u"I hate the word 'moist.'"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "moist")

    def test_word2(self):
        text = u"I hate the word hun tf"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "hun")

    def test_word3(self):
        text = u"“@BoobsNBamboos_: I hate the word hun tf” Sorry Hun."
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, None)

    def test_word4(self):
        text = u"!!!! RT @BoobsNBamboos_: I hate the word hun tf"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, None)

    def test_word5(self):
        text = u'RT @MegannoConnor: I hate the word "swills"'
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, None)

    def test_word6(self):
        text = u'I hate the word "Bae". It makes you sound uneducated.'
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "bae")

    def test_word7(self):
        text = u"Wow..I hate the word thot but that was funny."
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "thot")

    def test_word8(self):
        text = u"Why I hate the word 'couture'?! #weird"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "couture")

    def test_word9(self):
        text = (u'I hate the word "spooky", bro the fuck you mean '
                '" dis nigga movin spooky" sounds like some shaggy '
                'n scooby doo type shit son')
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "spooky")

    def test_word10(self):
        text = u'I swear I hate the word “ flee " . . . .'
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "flee")

    def test_word11(self):
        text = (u'I HATE the word bae....'
                'it seems like you just too lazy to say babe')
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "bae")

    def test_word12(self):
        text = u'I hate the word YALL like im a conjoined twin'
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "yall")

    def test_word13(self):
        text = u"I hate the word 'Banter' it annoys me so much🙈"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "banter")

    def test_word14(self):
        text = u"I hate the word madting"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "madting")

    def test_word15(self):
        text = (u"I hate the word ❌NO❌ like y'all nigga hate a bitch dat "
                "uses her teeth on da dick.")
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "no")

    def test_word16(self):
        text = (u"@QuayNastyy Lmao So What Would Call Me ? "
                "Cause I HATE The Word Boo .")
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "boo")

    def test_word17(self):
        text = u"i hate the word expand"
        word = word_tools.word_from_text(text, self.pattern, self.search_term)
        self.assertEqual(word, "expand")

    def test_word18(self):
        text = u"i hate the word glove(s)"
        word = word_tools.word_from_text(
            text, self.pattern, self.search_term)
        self.assertNotEqual(word, "glove(s")

    def test_word19(self):
        # Arrange
        self.setup_aint_a_word()
        text = u'"People(s)" ain\'t a word😒'

        # Act
        word = word_tools.word_from_text(
            text, self.pattern, self.search_term)

        # Assert
        self.assertNotEqual(word, "people(s")

    def test_word20(self):
        # Arrange
        self.setup_aint_a_word()
        text = u'"You(s)"\nAin\'t a word either 😒"'

        # Act
        word = word_tools.word_from_text(
            text, self.pattern, self.search_term)
        self.assertNotEqual(word, "you(s")

    def test_add_string_to_wordnik(self):
        words = ['string']
        wordlist_permalink = "test--47"
        word_tools.add_to_wordnik(words, wordlist_permalink)

    def test_add_strings_to_wordnik(self):
        words = ['string2', 'string3']
        wordlist_permalink = "test--47"
        word_tools.add_to_wordnik(words, wordlist_permalink)

    def test_add_unicode_to_wordnik(self):
        words = [u'unicode']
        wordlist_permalink = "test--47"
        word_tools.add_to_wordnik(words, wordlist_permalink)

    def test_add_unicodes_to_wordnik(self):
        words = [u'unicode2', u'unicode3']
        wordlist_permalink = "test--47"
        word_tools.add_to_wordnik(words, wordlist_permalink)

    def test_add_mix_to_wordnik(self):
        words = ['string4', u'unicode4']
        wordlist_permalink = "test--47"
        word_tools.add_to_wordnik(words, wordlist_permalink)


if __name__ == '__main__':
    unittest.main()
