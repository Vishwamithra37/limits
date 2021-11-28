from abc import abstractmethod
import threading
from typing_extensions import Protocol

from limits.storage.registry import StorageRegistry


class Storage(metaclass=StorageRegistry):
    """
    Base class to extend when implementing a storage backend.
    """

    def __init__(self, uri: str = None, **options):
        self.lock = threading.RLock()

    @abstractmethod
    def incr(self, key: str, expiry: int, elastic_expiry=False):
        """
        increments the counter for a given rate limit key

        :param str key: the key to increment
        :param int expiry: amount in seconds for the key to expire in
        :param bool elastic_expiry: whether to keep extending the rate limit
         window every hit.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, key):
        """
        :param str key: the key to get the counter value for
        """
        raise NotImplementedError

    @abstractmethod
    def get_expiry(self, key):
        """
        :param str key: the key to get the expiry for
        """
        raise NotImplementedError

    @abstractmethod
    def check(self):
        """
        check if storage is healthy
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        """
        reset storage to clear limits
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self, key):
        """
        resets the rate limit key
        :param str key: the key to clear rate limits for
        """
        raise NotImplementedError


class SupportsFixedWindow(Protocol):
    def incr(self, key, expiry, elastic_expiry=False):
        ...

    def get(self, key):
        ...

    def get_expiry(self, key):
        ...

    def check(self):
        ...

    def reset(self):
        ...

    def clear(self, key):
        ...


class SupportsMovingWindow(Protocol):
    def acquire_entry(self, key, limit, expiry, no_add=False):
        ...

    def get_num_acquired(self, key, expiry):
        ...

    def get_moving_window(self, key, limit, expiry):
        ...
