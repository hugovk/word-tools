#!/usr/bin/env python
"""
Show the most common words of a newline-separated word list
"""
import argparse

# Add thousands commas
def commafy(value):
    return "{:,}".format(value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show the most common words of a newline-separated word list",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infile',
        help='Input filename')
    parser.add_argument('-n', '--number', type=int, default=10,
        help="Show this number of most-common words")
    args = parser.parse_args()

    word_list = open(args.infile).read().splitlines()
    from collections import Counter
    counter = Counter(word_list)
    most_common = counter.most_common(args.number)

    print args.infile, "contains", commafy(len(word_list)), "words and", commafy(len(counter.most_common())), "unique words.\nThe top", commafy(args.number), "words are:"
    for i, (word, count) in enumerate(most_common):
        print commafy(i+1) + ".", word, "(" + commafy(count) + ")"

# End of file
