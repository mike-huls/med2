import time
import unittest

from expiring_lru_cache.caches.caches import TTLCache


class TestExpiringLRUCache(unittest.TestCase):

    def test_expiration(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        time.sleep(0.3)
        self.assertEqual(cache.get("a"), 1, msg="Failed to retrieve value '1' for key 'a' before expiration")
        time.sleep(0.3)
        self.assertIsNone(cache.get("a"), msg="Expected None after expiration of key 'a'")

    def test_cache_eviction_after_expiration(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        cache.put("b", 2)
        time.sleep(0.6)  # Both "a" and "b" should expire
        cache.put("c", 3)  # Should not evict "a" or "b" since they are expired
        self.assertIsNone(cache.get("a"), msg="Key 'a' should have expired and be None")
        self.assertIsNone(cache.get("b"), msg="Key 'b' should have expired and be None")
        self.assertEqual(cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'")

    def test_cache_retains_valid_entries(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        cache.put("b", 2)
        time.sleep(0.3)
        cache.put("c", 3)  # Should evict "a" as "b" is more recently used and not expired
        self.assertIsNone(cache.get("a"), msg="Key 'a' should have been evicted")
        self.assertEqual(cache.get("b"), 2, msg="Key 'b' should be retained as it is still valid")
        self.assertEqual(cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'")

    def test_no_expiration_for_recently_accessed(self):
        cache = TTLCache(capacity=2, ttl_seconds=0.5)
        cache.put("a", 1)
        time.sleep(0.3)
        cache.get("a")  # Accessing "a" should not refresh its expiration time
        time.sleep(0.3)
        self.assertIsNone(cache.get("a"), msg="Key 'a' should have expired despice being accessed recently")

    def test_mixed_operations_with_expiration(self):
        cache = TTLCache(capacity=3, ttl_seconds=0.4)
        cache.put("a", 1)
        print(cache.cache)
        time.sleep(0.2)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 1, msg="Key 'a' should still be available")
        time.sleep(0.3)
        self.assertIsNone(cache.get("a"), msg="Key 'a' should have expired after 0.4 seconds")
        self.assertEqual(cache.get("b"), 2, msg="Key 'b' should still be available")
        cache.put("d", 4)
        cache.put("e", 4)  # Should evict "c" as it is the least recently used
        self.assertIsNone(cache.get("c"), msg="Key 'c' should have been evicted")
        self.assertEqual(cache.get("b"), 2, msg="Key 'b' should still be available after adding 'd'")
        self.assertEqual(cache.get("d"), 4, msg="Failed to retrieve value '4' for key 'd'")
        time.sleep(0.4)

if __name__ == '__main__':
    unittest.main()
