#!/usr/bin/env python
"""
Show the most common words of a newline-separated word list
"""
from collections import Counter


# Add thousands commas
def commafy(value):
    return "{:,}".format(value)


def most_frequent_words_and_counts(word_list, number=None):
    counter = Counter(word_list)
    most_common = counter.most_common(number)
    return most_common


def most_frequent_words(word_list, number=None):
    words = [ite for ite, it in most_frequent_words_and_counts(
        word_list, number)]
    return words


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Show the most common words of a newline-separated "
                    "word list",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'infile',
        help='Input filename')
    parser.add_argument(
        '-n', '--number', type=int, default=10,
        help="Show this number of most-common words")
    args = parser.parse_args()

    word_list = open(args.infile).read().splitlines()
    most_common = most_frequent_words_and_counts(word_list, args.number)

    print(
        args.infile + " contains " + commafy(len(word_list)) + " words and " +
        commafy(len(most_frequent_words_and_counts(word_list))) +
        " unique words.\nThe top " + commafy(args.number) + " words are: ")
    for i, (word, count) in enumerate(most_common):
        print(commafy(i+1) + ". " + word + " (" + commafy(count) + ")")

# End of file
