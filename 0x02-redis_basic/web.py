#!/usr/bin/env python3
import requests
import redis
import time
from functools import wraps

# Redis client
redis_client = redis.Redis()

def count_calls(method):
    """
    Decorator that tracks the number of times a function is called with a specific URL.
    Uses Redis to store and retrieve the count.
    """
    @wraps(method)
    def wrapper(url):
        count_key = f"count:{url}"
        count = redis_client.get(count_key)
        if count:
            count = int(count)
            count += 1
        else:
            count = 1
        redis_client.setex(count_key, 10, str(count))
        return method(url)

    return wrapper


def get_page(url):
    """
    Retrieves the HTML content of a given URL.

    Args:
        url: The URL of the page to retrieve.

    Returns:
        The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
