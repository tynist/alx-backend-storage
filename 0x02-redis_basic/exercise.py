#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

UnionOfTypes = Union[str, bytes, int, float]


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

    def count_calls(method: Callable) -> Callable:
        """
        Decorator that counts the number of times a method is called.

        Args:
            method: The method being decorated.

        Returns:
            The wrapped method.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    def replay(self, method: Callable) -> None:
        """
        Displays the history of calls for a particular function.

        Args:
            method: The method to display the history for.
        """
        key = method.__qualname__
        calls = int(self._redis.get(key) or 0)

        print(f"{key} was called {calls} times:")

        for i in range(calls):
            input_key = f"{key}:input:{i}"
            output_key = f"{key}:output:{i}"

            inputs = self._redis.get(input_key).decode("utf-8")
            output = self._redis.get(output_key).decode("utf-8")

            print(f"{key}(*{inputs}) -> {output}")

    @count_calls
    def store(self, data: UnionOfTypes) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            data to be stored. Can be of type str, bytes, int, or float.

        Returns:
            The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Gets the stored data from Redis and may apply a conversion func

        Args:
            key: The key used to retrieve the data from Redis.
            fn: Optional conversion function to apply to the retrieved data.

        Returns:
            Retrieved data, may converted based on d given conversion func
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

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves an integer from Redis.

        Args:
            key: The key used to retrieve the data from Redis.

        Returns:
            The retrieved data as an integer.
        """
        return self.get(key, fn=int)
