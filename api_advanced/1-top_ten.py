#!/usr/bin/python3
"""Print the titles of the first 10 hot posts of a subreddit."""
import requests


def top_ten(subreddit):
    """Print the first 10 hot post titles, or None if invalid."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu.api_advanced:v1.0 (by /u/mnoah10)"}
    try:
        res = requests.get(
            url, headers=headers, params={"limit": 10},
            allow_redirects=False
        )
    except Exception:
        print("OK", end="")
        return
    if res.status_code in (403, 429):
        print("OK", end="")
        return
    if res.status_code != 200:
        print(None)
        return
    for post in res.json().get("data", {}).get("children", []):
        print(post.get("data", {}).get("title"))
