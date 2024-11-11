import time
from functools import wraps
from typing import Callable, Generator


def timer(name: str) -> Generator:
    try:
        print(f"TIMER:   {name} start")
        strt = time.perf_counter()
        yield
    finally:
        print(f"TIMER:   {name} finished in {time.perf_counter() - strt}")


class TimerCTX:
    func: Generator  # the function we're decorating with @contextmanager; must be a generator

    def __init__(self, func, *args, **kwargs):
        self.func = func(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return next(self.func)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


with TimerCTX(func=timer, name="testname") as timer:
    # pass
    print("doing something else")


##################################33 ADD __CALL__
def timer_normal(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def decorator_implementation(*args, **kwargs):
            try:
                strt = time.perf_counter()
                return func(*args, **kwargs)
            finally:
                print(f"TIMER:   {name} finished in {time.perf_counter() - strt}")

        return decorator_implementation

    return decorator


class MyContextManager:
    def __init__(self, func, *args, **kwargs):
        print(func, args, kwargs)
        self.gen = func(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        print(args, kwargs)
        return next(self.gen(name="jojojo"))

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, func):
        print(func)

        @wraps(func)
        def inner(*args, **kwds):
            with self:
                return func(*args, **kwds)

        return inner


@MyContextManager(name="dec")
def timer(name: str) -> Generator:
    strt = time.perf_counter()
    try:
        print(f"TIMER:   {name} start")
        yield
    finally:
        print(f"TIMER:   {name} finished in {time.perf_counter() - strt}")


@timer(name="dec")
def ding():
    print("in ding")


# with timer(name='testname'):
with timer:
    # pass
    print("doing something else")
