#!/usr/bin/env python3

"""
Writing strings to Redis
"""

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self) -> None:
        """
        Initialize the cache with a Redis instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, float, int]) -> str:
        """
        Store data in Redis using a random key generated by uuid4.
        Returns the key as a string.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)
        return rand_key
