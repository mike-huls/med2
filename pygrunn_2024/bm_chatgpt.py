import timeit


def my_func(a, b, c):
    pass


# Test with positional arguments
time_pos = timeit.timeit("my_func(1, 2, 3)", globals=globals(), number=1000000)

# Test with keyword arguments
time_kw = timeit.timeit("my_func(a=1, b=2, c=3)", globals=globals(), number=1000000)

print(f"Positional args time: {time_pos}")
print(f"Keyword args time: {time_kw}")
