from typing import Any

from .i_eviction_policy import ICacheStrategy


class LRUEvictionPolicy(ICacheStrategy):
    def on_access(self, cache: "BaseCache", key: Any) -> Any:
        """Move the accessed item to the end to mark it as most recently used."""
        cache.cache.move_to_end(key=key)
        # return cache.cache.get(key)

    def on_insert(self, cache: "BaseCache", key: Any) -> None:
        """If the cache is at capacity, evict the least recently used item."""
        if len(cache.cache) >= cache.capacity:
            cache.cache.popitem(last=False)

    def evict(self, cache: "BaseCache") -> None:
        """Evict the least recently used item."""
        if cache.cache:
            cache.cache.popitem(last=False)
