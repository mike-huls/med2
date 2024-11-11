from contextlib import contextmanager


@contextmanager
def my_decorator():
    print("Setup")
    yield
    print("Teardown")


@my_decorator()
def say_hello():
    print("hello")


say_hello()


def my_decorator():
    print("Setup")
    yield
    print("Teardown")


# contextmanager(my_decorator(say_hello()))


def decorator_function():
    print("before function")
    yield
    print("after function")


@decorator_function()
def my_func():
    print("I'm the main function")


print("with dec")
decorator_function()
print("functions:")
contextmanager(decorator_function())
