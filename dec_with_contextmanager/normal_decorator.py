import logging
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger("logger")


def timer_normal(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def decorator_implementation(*args, **kwargs):
            strt = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                print(f"TIMER:   {name} finished in {time.perf_counter() - strt}")

        return decorator_implementation

    return decorator
