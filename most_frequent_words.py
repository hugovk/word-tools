#!/usr/bin/env python
"""
Show the most common words of a newline-separated word list
"""
import argparse

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

    print args.infile, "contains", len(word_list), "words and the top", args.number, "words are:"
    for i, (word, count) in enumerate(most_common):
        print str(i+1) + ".", word, "(" + str(count) + ")"

# End of file
