#!/usr/bin/env python
# encoding=utf8
"""
Show the number of mentions per month for a word:
    word_usage -w twizzle
    word_usage -w bae -y 2014
    word_usage -w twizzle -s favorite
    word_usage -w twizzle -s favourite
"""
from __future__ import print_function
from most_frequent_words import commafy
import argparse
from word_charts import load_csv, filter_year, filter_search_term
from collections import OrderedDict


def filter_word(tweets, desired_word):
    found = []
    for tweet in tweets:
        if desired_word == tweet["word"]:
            found.append(tweet)
    print("Total " + desired_word + ":\t" + commafy(len(found)))
    return found


def print_per_month(tweets):
    counts = OrderedDict()
    for tweet in tweets:
        year = tweet["created_at"][-4:]
        month = tweet["created_at"][4:7]
        month_year = month + " " + year
        if month_year not in counts:
            counts[month_year] = 0
        counts[month_year] += 1

    # from pprint import pprint
    xs, ys = [], []
    for month_year in counts:
        print(month_year, counts[month_year])
        xs.append(month_year)
        ys.append(counts[month_year])

    return xs, ys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Show the number of mentions per month for a word.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-c', '--csv', default='M:/bin/data/all.csv',
        help='Input CSV file')
    parser.add_argument(
        '-w', '--word',  default='bae',
        help='Word to search for')
    parser.add_argument(
        '-y', '--year',  type=int, default=None,
        help="Only from this year")
    parser.add_argument(
        '-ny', '--not_year',  type=int, default=None,
        help="Not from this year")
    parser.add_argument(
        '-s', '--search_term',
        help="Only for this search term")
    parser.add_argument(
        '-p', '--plot', action='store_true',
        help="Create a bar graph of results (requires Plotly authentication: "
             "https://plot.ly/python/getting-started/")
    args = parser.parse_args()

    tweets = load_csv(args.csv)
    print("Total tweets:\t" + commafy(len(tweets)))

    tweets = filter_word(tweets, args.word)

    if args.search_term:
        tweets = filter_search_term(tweets, args.search_term)

    if args.year:
        tweets = filter_year(tweets, args.year)

    if args.not_year:
        tweets = filter_year(tweets, args.not_year, invert_filter=True)

    # Sort by ID = sort chronologically
    tweets = sorted(tweets, key=lambda k: k['id_str'])

    xs, ys = print_per_month(tweets)

    if args.plot:
        print("Plotting...")
        import plotly.plotly as py  # pip install plotly + needs auth
        import plotly.graph_objs as go
        layout = go.Layout(
            title=args.word
        )
        trace0 = go.Scatter(
            x=xs,
            y=ys,
            mode='lines+markers',
            name=args.word
        )
        data = [trace0]
        fig = go.Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename='word_usage_' + args.word)
        print(plot_url)

# End of file
