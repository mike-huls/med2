import math
import typing


class BloomFilter:
    expected_number_of_items: int
    desired_fp_rate: float
    size: int
    num_hashes: int
    bit_array: list[int]

    def __init__(self, expected_number_of_items: int, desired_false_positive_rate: float) -> None:
        self.expected_number_of_items: int = expected_number_of_items
        self.desired_fp_rate: float = desired_false_positive_rate
        self.size: int = self._calculate_optimal_size(expected_number_of_items, desired_false_positive_rate)
        self.num_hashes: int = self._calculate_optimal_num_hashes(self.size, expected_number_of_items)
        self.bit_array: list[int] = [0] * self.size

    def _calculate_optimal_size(self, n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    def _calculate_optimal_num_hashes(self, m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return int(k)

    def _hashes(self, item: str) -> typing.Iterable[int]:
        """Responsible for hashing the item"""
        for i in range(self.num_hashes):
            yield hash(f"{item}{i}") % self.size

    def add(self, item: str) -> None:
        """Takes the outputs of the hash functions and sets the corresponding bits in the bit array"""
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def contains(self, item: str) -> bool:
        """Checks if all bit-indices from the hash functions are set to 1 in the bit array; only then the item may be contained"""
        for hash_value in self._hashes(item=item):
            if not self.bit_array[hash_value]:
                return False
        return True


# Example usage
if __name__ == "__main__":
    expected_number_of_items = 1000  # Expected number of items to add
    desired_fp_rate = 0.05  # Desired false positive rate

    bloom = BloomFilter(expected_number_of_items, desired_fp_rate)

    print(bloom.num_hashes)
    print(len(bloom.bit_array))

    # Add some values
    bloom.add("apple")
    bloom.add("banana")

    # Lookup values
    print("apple:", bloom.contains("apple"))  # Should return True
    print("banana:", bloom.contains("banana"))  # Should return True
    print("cherry:", bloom.contains("cherry"))  # Might return False, but can return True (false positive)

    def _hashes(item: str, num_hashes: int, bitarray_size: int) -> typing.Iterable[int]:
        """Hashes item, yields bit array indices"""
        for i in range(num_hashes):
            yield hash(f"{item}{i}") % bitarray_size

    for index in _hashes(item="my_value", num_hashes=6, bitarray_size=10_000):
        print("index: ", index)

    print([i for i in _hashes(item="my_value", num_hashes=6, bitarray_size=10_000)])
