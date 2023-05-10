import redis
import uuid
from typing import Union

UnionOfTypes = Union[str, bytes, int, float]

class Cache:
    """
    Cache class that stores data in Redis.
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
            data: The data to be stored. Can be of type str, bytes, int, or float.

        Returns:
            The randomly generated key used to store the data.

        Example:
            cache = Cache()
            data = b"hello"
            key = cache.store(data)
            print(key)
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
