#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    Increments the count for the method's qualified name in Redis.
    Returns the value returned by the original method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

class Cache:
    """
    Cache class that stores data in Redis and provides retrieval methods.
    """

    def __init__(self):
        """
        Initializes the Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: UnionOfTypes) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            stored data can be of type str, bytes, int, or float.

        Returns:
            The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves the stored data from Redis and optionally applies a conversion function.

        Args:
            key: The key used to retrieve the data from Redis.
            fn: Optional conversion function to apply to the retrieved data.

        Returns:
            The retrieved data, optionally converted based on the provided conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a UTF-8 string from Redis.

        Args:
            key: The key used to retrieve the data from Redis.

        Returns:
            The retrieved data as a UTF-8 string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer from Redis.

        Args:
            key: The key used to retrieve the data from Redis.

        Returns:
            The retrieved data as an integer.
        """
        return self.get(key, fn=int)
