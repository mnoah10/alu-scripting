#!/usr/bin/python3
"""Recursively collect the titles of all hot posts of a subreddit."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of all hot post titles, or None if invalid."""
    if hot_list is None:
        hot_list = []
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
            return None
        data = res.json().get("data", {})
    except Exception:
        return None
    for post in data.get("children", []):
        hot_list.append(post.get("data", {}).get("title"))
    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    return hot_list
