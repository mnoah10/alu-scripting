#!/usr/bin/python3
"""Recursively count keywords in the hot post titles of a subreddit."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of keywords found in hot post titles."""
    if counts is None:
        counts = {}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu.api_advanced:v1.0 (by /u/mnoah10)"}
    params = {"limit": 100}
    if after:
        params["after"] = after
    try:
        res = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )
        if res.status_code != 200:
            return
        data = res.json().get("data", {})
    except Exception:
        return
    words = [w.lower() for w in word_list]
    for post in data.get("children", []):
        title = post.get("data", {}).get("title", "")
        for token in title.lower().split():
            if token in words:
                counts[token] = counts.get(token, 0) + 1
    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, after, counts)
    results = []
    for word, found in counts.items():
        total = found * words.count(word)
        if total > 0:
            results.append((word, total))
    results.sort(key=lambda item: (-item[1], item[0]))
    for word, total in results:
        print("{}: {}".format(word, total))
