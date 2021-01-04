#!/usr/bin/env python3
"""
Get top word charts from a CSV file of logged tweets:
    word_charts.py -n 100
Get top in a given year:
    word_charts.py -y 2014 -n 100
Get top in a given year that aren't in the previous year.
    word_charts.py -y 2014 -n 100 --diff
Get top for a search term:
    word_charts.py  -s favorite
    word_charts.py  -s favourite
"""
from most_frequent_words import most_frequent_words_and_counts, commafy
import argparse
import csv


def filter_year(tweets, desired_year, invert_filter=False):
    found = []
    for tweet in tweets:
        year = int(tweet["created_at"][-4:])
        if invert_filter:
            if desired_year != year:
                found.append(tweet)
        else:
            if desired_year == year:
                found.append(tweet)
    print("Total in " + str(desired_year) + ":\t" + commafy(len(found)))
    return found


def filter_search_term(tweets, desired_search_term):
    found = []
    for tweet in tweets:
        if desired_search_term in tweet["search_term"]:
            found.append(tweet)
    print("Total " + desired_search_term + ":\t" + commafy(len(found)))
    return found


def print_chart(top):
    """
    param top: a list of (word, count) tuples.
    """
    if args.html:
        print("<ol>")

    for i, (word, count) in enumerate(top):
        if args.html:
            print("<li>{} ({})</li>".format(word, commafy(count)))
        else:
            print(str(i + 1) + ". " + word + " (" + commafy(count) + ")")

    if args.html:
        print("</ol>")


def print_top(tweets, number=10, year=None, search_term=None):
    words = []

    if search_term:
        tweets = filter_search_term(tweets, search_term)

    if year:
        tweets = filter_year(tweets, year)

    for tweet in tweets:
        words.append(tweet["word"])

    print()
    title = "# Top " + str(number)
    if year:
        title += " (" + str(year) + ")"
    print(title)
    print()

    # Filter out "ｆａｔｅ"
    words = list(filter(("ｆａｔｅ").__ne__, words))

    top = most_frequent_words_and_counts(words, number)
    print_chart(top)
    return top


# cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode("utf-8"))


def load_csv(filename):
    # with codecs.open(filename, mode='rb', encoding='cp1252') as fd:
    with open(filename, mode="r") as fd:
        data = csv.DictReader(fd)
        rows = []
        seen = set()  # avoid duplicates
        for row in data:
            if row["id_str"] not in seen and row["word"] not in ["actually"]:
                seen.add(row["id_str"])
                rows.append(row)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get top word charts from a CSV file of logged tweets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c", "--csv", default="M:/bin/data/favibot.csv", help="Input CSV file"
    )
    parser.add_argument("-n", "--top-number", type=int, default=10, help="Show top X")
    parser.add_argument(
        "-y", "--year", type=int, default=None, help="Only from this year"
    )
    parser.add_argument("-s", "--search_term", help="Only for this search term")
    parser.add_argument(
        "--diff", action="store_true", help="Compare a year to a previous year"
    )
    parser.add_argument(
        "-yd",
        "--yeardiff",
        type=int,
        default=1,
        help="Number of years to compare against",
    )
    parser.add_argument("--html", action="store_true", help="Output with html markup")
    args = parser.parse_args()

    tweets = load_csv(args.csv)
    print("Total tweets:\t" + commafy(len(tweets)))

    if args.diff and args.year:
        last_year = print_top(
            tweets,
            number=args.top_number,
            year=args.year - args.yeardiff,
            search_term=args.search_term,
        )
        print()
        this_year = print_top(
            tweets, number=args.top_number, year=args.year, search_term=args.search_term
        )
        last_years_words = [e[0] for e in last_year]
        this_years_words = [e[0] for e in this_year]

        set1 = set(last_years_words)
        diff = [x for x in this_years_words if x not in set1]

        top = []
        for word in diff:
            for e in this_year:
                if e[0] == word:
                    top.append(e)
                    continue
        print()
        top_x = " top " + str(args.top_number)
        print(
            "# New entries in the "
            + str(args.year)
            + top_x
            + " which weren't in the "
            + str(args.year - args.yeardiff)
            + top_x
        )
        print()
        print_chart(top)

    else:
        print_top(
            tweets, number=args.top_number, year=args.year, search_term=args.search_term
        )


# End of file
