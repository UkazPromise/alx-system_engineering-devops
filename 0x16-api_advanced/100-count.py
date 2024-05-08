#!/usr/bin/python3
""" raddit api"""

import json
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    """Count occurrences of keywords in titles of hot articles from a subreddit."""
    if counts is None:
        counts = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'after': after} if after else {}

    response = requests.get(url, params=params, headers={'User-Agent': 'bhalut'}, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()['data']
        for child in data['children']:
            title = child['data']['title'].lower()
            for word in word_list:
                if word.lower() in title.split():
                    counts[word.lower()] = counts.get(word.lower(), 0) + 1

        after = data.get('after')
        if after:
            return count_words(subreddit, word_list, after, counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
    elif response.status_code == 404:
        print("Invalid subreddit.")
    else:
        print("Error:", response.status_code)

# Example usage
if __name__ == "__main__":
    subreddit = input("Enter subreddit: ")
    words = input("Enter words separated by space: ").split()
    count_words(subreddit, words)
