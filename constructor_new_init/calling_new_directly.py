tuple1 = tuple((1, 2))  # --> (1, 2)
tuple2 = tuple.__new__(tuple, (1, 2))  # --> (1, 2)


int1 = int("1")  # --> 1`
int2 = int.__new__(int, "1")  # --> (1, 2)
int3 = int.__new__(int).__init__("1")

print(int1)
print(int2)
print(int3)
