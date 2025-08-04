#!/usr/bin/python3
"""Module that recursively counts keyword occurrences in hot Reddit posts."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Recursively count occurrences of keywords in a subreddit's hot post titles."""
    if counts is None:
        # Normalize word_list: lowercase, handle duplicates
        counts = {}
        for word in word_list:
            word = word.lower()
            counts[word] = counts.get(word, 0)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'custom-agent'}
    params = {'after': after, 'limit': 100}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    children = data.get("children", [])

    for post in children:
        title_words = post.get("data", {}).get("title", "").lower().split()
        for word in title_words:
            if word in counts:
                counts[word] += 1

    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, after, counts)

    # Filter out 0s
    filtered = {k: v for k, v in counts.items() if v > 0}
    sorted_counts = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))

    for word, count in sorted_counts:
        print(f"{word}: {count}")
