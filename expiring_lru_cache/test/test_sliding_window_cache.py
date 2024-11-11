import unittest
import time

from expiring_lru_cache.caches.caches import SlidingWindowCache


class TestSlidingWindowEvictionPolicy(unittest.TestCase):

    def test_sliding_window_no_expiration_within_window(self):
        # Create a sliding window cache with a 0.5-second window size
        sliding_cache = SlidingWindowCache(capacity=3, expiration_seconds=0.5)

        sliding_cache.put("a", 1)
        time.sleep(0.3)
        self.assertEqual(sliding_cache.get("a"), 1, msg="Key 'a' should still be available within the window")

        time.sleep(0.2)
        self.assertEqual(sliding_cache.get("a"), 1, msg="Key 'a' should still be available as it was accessed within the window")

    def test_sliding_window_expiration(self):
        # Create a sliding window cache with a 0.5-second window size
        sliding_cache = SlidingWindowCache(capacity=3, expiration_seconds=0.2)
        sliding_cache.put("a", 1)

        time.sleep(0.1)
        sliding_cache.get(key="a")
        time.sleep(0.15)
        self.assertEqual(sliding_cache.cache.get("a"), second=1, msg="Key 'a' should not have expired after the window size")
        time.sleep(0.1)

        self.assertIsNone(obj=sliding_cache.get("a"), msg="Key 'a' should have been expired by now")

    def test_sliding_window_refresh_on_access(self):
        # Create a sliding window cache with a 0.5-second window size
        sliding_cache = SlidingWindowCache(capacity=3, expiration_seconds=0.5)

        sliding_cache.put("a", 1)
        time.sleep(0.3)
        sliding_cache.get("a")  # Accessing "a" should refresh its window

        time.sleep(0.3)
        self.assertEqual(sliding_cache.get("a"), 1, msg="Key 'a' should not have expired as it was accessed recently")

    def test_sliding_window_eviction_after_insert(self):
        # Create a sliding window cache with a 0.5-second window size
        sliding_cache = SlidingWindowCache(capacity=2, expiration_seconds=0.5)

        sliding_cache.put("a", 1)
        sliding_cache.put("b", 2)
        time.sleep(0.3)
        sliding_cache.put("c", 3)  # This should evict "a" as it is the least recently used within the window

        self.assertIsNone(sliding_cache.get("a"), msg="Key 'a' should have been evicted as it was least recently used")
        self.assertEqual(sliding_cache.get("b"), 2, msg="Key 'b' should still be available")
        self.assertEqual(sliding_cache.get("c"), 3, msg="Failed to retrieve value '3' for key 'c'")

    def test_sliding_window_mixed_operations(self):
        # Create a sliding window cache with a 0.4-second window size
        sliding_cache = SlidingWindowCache(capacity=3, expiration_seconds=0.4)

        sliding_cache.put("a", 1)
        time.sleep(0.2)
        sliding_cache.put("b", 2)
        sliding_cache.put("c", 3)

        print(sliding_cache.cache)
        self.assertEqual(sliding_cache.cache.get("a"), 1, msg="Key 'a' should still be available")

        time.sleep(0.3)
        self.assertIsNone(sliding_cache.get("a"), msg="Key 'a' should have expired after 0.4 seconds")
        self.assertEqual(sliding_cache.get("b"), 2, msg="Key 'b' should still be available")

        sliding_cache.put("d", 4)
        sliding_cache.put("e", 4)  # This should evict "c" as it is the least recently used within the window
        self.assertIsNone(sliding_cache.get("c"), msg="Key 'c' should have been evicted")
        self.assertEqual(sliding_cache.get("b"), 2, msg="Key 'b' should still be available after adding 'd'")
        self.assertEqual(sliding_cache.get("d"), 4, msg="Failed to retrieve value '4' for key 'd'")


if __name__ == '__main__':
    unittest.main()
