import time
from functools import wraps
from typing import Generator

from contextlib import contextmanager


@contextmanager
def timer(name: str) -> Generator:
    try:
        print(f"TIMER:   {name} start")
        strt = time.perf_counter()
        yield
    finally:
        print(f"TIMER:   {name} finished in {time.perf_counter() - strt}")


@timer(name="test")
def fn_with_ctx_decorator(name: str, age: int) -> str:
    return f"{name} is {age} years old"


# fn_with_ctx_decorator(name="mike", age=34)


# print(dir(contextmanager))
# print(contextmanager.__annotations__)
# print(contextmanager.__call__(fn_with_ctx_decorator)(name="mike", age=34))
# print('-->', next(contextmanager.__call__(fn_with_ctx_decorator)(name="mike", age=34)))


def make_generator():
    def helper(*args, **kwds):
        return "hallo"

    return helper


# print(next(make_generator()))


def generator_func(number: int) -> Generator:
    for i in range(number):
        print(f"go {i}")
        yield i
        print("after yield")
    print("after loop")


gen = generator_func(number=5)
print("__init")
print(next(gen))
print(" ")
print(next(gen))
print(next(gen))
print(next(gen))
