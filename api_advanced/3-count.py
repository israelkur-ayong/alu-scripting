#!/usr/bin/python3
"""Module that recursively counts keyword occurrences in hot Reddit posts."""
import requests
import re


def count_words(subreddit, word_list, after=None, counts=None):
    """Recursively count word occurrences in hot titles of a subreddit."""
    if counts is None:
        counts = {}
        for word in word_list:
            word_lower = word.lower()
            counts[word_lower] = counts.get(word_lower, 0)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'custom-agent'}
    params = {'after': after, 'limit': 100}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])
    for post in posts:
        title = post.get("data", {}).get("title", "").lower()
        words = re.findall(r'\b\w+\b', title)
        for word in words:
            if word in counts:
                counts[word] += 1

    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, after, counts)

    # Prepare and print sorted results
    result = [(word, count) for word, count in counts.items() if count > 0]
    result.sort(key=lambda x: (-x[1], x[0]))
    for word, count in result:
        print(f"{word}: {count}")
