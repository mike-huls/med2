from abc import ABC, abstractmethod
from typing import Any


class ICacheStrategy(ABC):
    @abstractmethod
    def on_access(self, cache: "BaseCache", key: Any) -> None:
        """Method called when a key is accessed in the cache."""
        pass

    @abstractmethod
    def on_insert(self, cache: "BaseCache", key: Any) -> None:
        """Method called when a new key-value pair is inserted into the cache."""
        pass

    @abstractmethod
    def evict(self, cache: "BaseCache") -> None:
        """Method to evict an item based on the eviction policy."""
        pass
