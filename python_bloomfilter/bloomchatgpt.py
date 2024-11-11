from typing import List
import hashlib
import math


class BloomFilter:
    def __init__(self, items_count: int, fp_prob: float) -> None:
        self.size: int = self.get_size(items_count, fp_prob)
        print(f"{self.size=}")
        self.hash_count: int = self.get_hash_count(self.size, items_count)
        print(f"{self.hash_count=}")
        self.bit_array: List[int] = [0] * self.size
        print(f"{self.bit_array=}")

    def add(self, item: str) -> None:
        for i in range(self.hash_count):
            digest: int = self.hash(i, item)
            self.bit_array[digest % self.size] = 1

    def check(self, item: str) -> bool:
        for i in range(self.hash_count):
            digest: int = self.hash(i, item)
            if self.bit_array[digest % self.size] == 0:
                return False
        return True

    @staticmethod
    def get_size(n: int, p: float) -> int:
        m: float = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def get_hash_count(m: int, n: int) -> int:
        k: float = (m / n) * math.log(2)
        print(f"{k=}")
        return int(k)

    def hash(self, hash_number: int, item: str) -> int:
        hash_function = hashlib.sha256()
        hash_function.update(item.encode())
        return int(hash_function.hexdigest(), 16) + hash_number


# Example usage
bloom = BloomFilter(20, 0.05)
bloom.add("apple")
print("apple", bloom.check("apple"))  # Should return True
print("banana", bloom.check("banana"))  # Should return False
