import time
from functools import wraps
from typing import Generator, Callable


class my_contextmanager:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        # Create a generator from the generator function
        generator = self.func(*args, **kwargs)
        # Return an instance of _MyContextManager with the generator and the original function
        return _MyContextManager(generator, self.func, *args, **kwargs)


class _MyContextManager:
    def __init__(self, generator, func, *func_args, **func_kwargs):
        self.generator = generator
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

    def __enter__(self):
        return next(self.generator)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            next(self.generator)
        except StopIteration:
            pass

    def __call__(self, *args, **kwargs):
        # This method is called when the decorated function is invoked.
        # Wrap the function call within the context manager
        with self:
            return self.func(*args, **kwargs)


@my_contextmanager
def timer(name: str) -> Generator:
    start = time.perf_counter()
    try:
        print(f"TIMER: {name} start")
        yield
    finally:
        print(f"TIMER: {name} finished in {time.perf_counter() - start} seconds")


# Using as a context manager
with timer(name="testname"):
    print("doing something else")


# Using as a decorator
@timer(name="decorator test")
def do_something():
    print("doing something")


do_something()
