#!/usr/bin/env python3

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize the Redis client
r = redis.Redis()


def count_access(fn: Callable) -> Callable:
    """
    Decorator to count how many times a URL is accessed and cache the result.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        r.incr(f"count:{url}")

        # Check if the page is already cached
        cached_page = r.get(url)
        if cached_page:
            print(f"Cache hit for {url}")
            return cached_page.decode('utf-8')

        # Fetch the page content if not cached
        print(f"Fetching page from {url}")
        result = fn(url)

        # Cache the result with an expiration time of 10 seconds
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
    # Fetch the page multiple times to test caching and counting
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))

    # Check how many times the URL was accessed
    access_count = r.get(f"count:{url}").decode('utf-8')
    print(f"The URL {url} was accessed {access_count} times.")
