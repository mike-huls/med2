import math
import mmh3  # MurmurHash3
from bitarray import bitarray


class BloomFilter:
    items_count: int
    fp_rate: float
    size: int
    hash_count: int
    bit_array: bitarray

    def __init__(self, expected_number_of_items, desired_false_positive_rate):
        # Number of items expected to be stored in bloom filter
        self.items_count = expected_number_of_items
        # False Positive probability in decimal
        self.fp_rate = desired_false_positive_rate
        # Size of bit array to use
        self.size = self.optimal_memory_size(expected_number_of_items, desired_false_positive_rate)
        # Number of hash functions to use
        self.hash_count = self.optimal_n_hashes(self.size, expected_number_of_items)
        # Bit array of given size
        self.bit_array = bitarray(self.size)
        # Initialize all bits as 0
        self.bit_array.setall(0)

    def add_bulk(self, items):
        for item in items:
            self.add(item)

    def add(self, item):
        # digests = []
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = True

    def contains(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            if not self.bit_array[index]:
                return False
        return True

    @classmethod
    def optimal_memory_size(self, n: int, p: float) -> int:
        """Return the required size of bit array(m)
        m = -(n * lg(p)) / (lg(2)^2)
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def optimal_n_hashes(self, m: int, n: int) -> int:
        """
        Return the number of required hash functions
            k = (m/n) * lg(2)
        """
        k = (m / n) * math.log(2)
        return int(k)


# Example Usage
items_count = 20  # Number of items expected to add
fp_rate = 0.05  # False positive probability

bloom = BloomFilter(items_count, fp_rate)

# Add some elements
bloom.add("Hello")
bloom.add("World")

# Check for existence
print(bloom.contains("Hello"))  # True
print(bloom.contains("World"))  # True
print(bloom.contains("something else"))  # False
