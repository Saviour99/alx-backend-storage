#!/usr/bin/env python3

import requests
import redis
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_access(fn: Callable) -> Callable:
    """
    Decorator to count how many times a URL is accessed and cache the result.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")

        cached_page = r.get(url)
        if cached_page:
            print(f"Cache hit for {url}")
            return cached_page.decode('utf-8')

        print(f"Fetching page from {url}")
        result = fn(url)

        r.setex(url, 10, result)
        return result

    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches it for 10 seconds.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))

    access_count = r.get(f"count:{url}").decode('utf-8')
    print(f"The URL {url} was accessed {access_count} times.")
