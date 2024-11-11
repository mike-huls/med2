from typing import Callable


class Decorator:
    func: Callable

    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        print("before calling the function")
        self.func(*args, **kwargs)
        print("after calling the function")


@Decorator
def say_hello(name: str):
    print(f"hello {name}!")


say_hello(name="mike")

Decorator(say_hello(name="mike"))


@Decorator
def decorator_function():
    print("before function")
    yield
    print("after function")


decorator_function()
