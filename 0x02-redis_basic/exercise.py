import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

UnionOfTypes = Union[str, bytes, int, float]


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function in Redis.
    Appends input parameters to a list in Redis and stores the output in another list.
    """
    key = method.__qualname__
    inputs_key = f"{key}:inputs"
    outputs_key = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))
        return output

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

    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            data: The data to be stored. Can be of type str, bytes, int, or float.

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

    def replay(self, method: Callable) -> None:
        """
        Displays the history of calls for a particular function.

        Args:
            method: The method to display the history for.
        """
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"

        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)

        num_calls = len(inputs)

        print(f"{key} was called {num_calls} times:")
        for input_args, output_key in zip(inputs, outputs):
            print(f"{key}{input_args} -> {output_key}")
