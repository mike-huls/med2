import time

from dec_with_contextmanager.normal_decorator import timer_normal
from dec_with_contextmanager.with_contextlib import timer


@timer_normal(name="test")
def fn_with_normal_decorator(name: str, age: int) -> None:
    print(f"{name} is {age} years old")


@timer(name="AS DEC")
def fn_with_ctx_decorator(name: str, age: int) -> None:
    print(f"{name} is {age} years old")


# fn_with_normal_decorator(name="mike", age=34)
fn_with_ctx_decorator(name="mike", age=34)

# Additionally you can call it like this
with timer(name="ctx_manager"):
    print("In context-manager")


print("\nCOMBO")
with timer(name="as ctx"):
    fn_with_ctx_decorator(name="john", age=42)
    print("In context-manager")
