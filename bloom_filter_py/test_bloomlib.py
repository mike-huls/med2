from bloomlib import BloomFilter

# 1. Create the filter
bf = BloomFilter(expected_number_of_items=1_000, desired_false_positive_rate=0.05)

# 2. Add items
for i in range(100):
    bf.add(item=i)

# 3. Check if an item is contained; False means definitely not, True means "maybe"
if (bf.contains(item=42)):
    print("This item may be in filter")
else:
    print("This item is definitely not in the filter")


assert not bf.contains(item=25554656)
assert not bf.contains(item=101)
