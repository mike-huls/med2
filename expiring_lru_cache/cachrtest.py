from cachr import LRUCache

@LRUCache(capacity=2)
def add(i, y):
    print("ading")
    return i + y

print(add(1, 2))
print(add(1, 2))
print(add(1, 2))