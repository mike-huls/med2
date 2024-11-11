import time
from collections import OrderedDict
from typing import Any

from expiring_lru_cache.cache_strategies.i_eviction_policy import ICacheStrategy


class TTLEvictionPolicy(ICacheStrategy):
    def __init__(self, ttl_seconds: float):
        self.ttl = ttl_seconds  # Time-to-live in seconds
        self.timestamps: OrderedDict[Any, float] = OrderedDict()

    def _is_expired(self, key: Any) -> bool:
        """Check if the item is expired based on its timestamp."""
        return (time.time() - self.timestamps[key]) > self.ttl

    def on_access(self, cache: "BaseCache", key: Any) -> None:
        """Remove the item if it's expired, otherwise update its access time."""
        if self._is_expired(key):
            cache.cache.pop(key, None)
            self.timestamps.pop(key, None)
            return None
        cache.cache.move_to_end(key=key)


    def on_insert(self, cache: "BaseCache", key: Any) -> None:
        """Insert an item into the cache, evicting if necessary."""
        if len(cache.cache) >= cache.capacity:
            cache.cache.popitem(last=False)
        # cache.cache[key] = cache.cache[key]
        self.timestamps[key] = time.time()

    def evict(self, cache: "BaseCache") -> None:
        """Evict items based on expiration and capacity."""
        for key in (key for key in self.timestamps if self._is_expired(key)):
            cache.cache.pop(key, None)
            self.timestamps.pop(key, None)

        if len(cache.cache) >= cache.capacity:
            cache.cache.popitem(last=False)
