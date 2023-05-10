#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import redis
import time
from functools import wraps

# Redis client
redis_client = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """
    Decorator wrapper that tracks URL access count and caches results.
    """

    @wraps(fn)
    def wrapper(url):
        """
        Wrapper function for the decorator.
        Increments URL access count and checks for cached result.
        If cached result is available, returns it.
        Otherwise, call d original function, caches result and returns it.
        """

        # Increment the count for the URL
        redis_client.incr(f"count:{url}")

        # Check if the result is already cached
        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')

        # Call the original function to get the result
        result = fn(url)

        # Cache the result with an expiration time of 10 seconds
        redis_client.setex(f"cached:{url}", 10, result)
        return result
    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using the requests module.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the URL as a string.
    """
    response = requests.get(url)
    return response.text
