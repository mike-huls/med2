from typing import Any

from .i_eviction_policy import ICacheStrategy


class SimpleCache(ICacheStrategy):
    def on_access(self, cache: "BaseCache", key: Any) -> None:
        """Method called when a key is accessed in the cache."""
        # Does nothing; key order is maintained
        pass

    def on_insert(self, cache: "BaseCache", key: Any) -> None:
        """ Method called when a new key-value pair is inserted into the cache."""
        # Does nothing; key order is maintained
        pass

    def evict(self, cache: "BaseCache") -> None:
        """ Method to evict an item based on the eviction policy."""
        # Does nothing; key order is maintained; remove keys in order of insertion
        pass
