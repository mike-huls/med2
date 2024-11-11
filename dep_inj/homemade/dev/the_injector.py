import functools
import math
import time
from typing import Callable


class Inject:
    """
    A decorator that retries a function up to a given number of times with a given timeout.
    """

    func: Callable
    provide_in: str

    def __init__(self, provide_in: str = "root"):
        self.provide_in = provide_in

    def __call__(self, func: Callable, *args, **kwargs):
        @functools.wraps(func)  # This applies the wraps decorator to preserve func's metadata
        def wrapper(*args, **kwargs):
            functools.update_wrapper(self, func)  ## TA-DA! ##

            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.debug(msg=f"Unable to execute {func.__name__}: {e}. Trying again after {self.timeout_seconds} seconds")
                    self.__current_try += 1
                    if self.__current_try >= self.max_tries:
                        raise ValueError(f"Exceeded max tries trying to execute {func.__name__}: {e}")

                    if self.timeout_seconds <= 1:
                        time.sleep(self.timeout_seconds)
                    else:
                        logger.debug(f"sleeping {math.ceil(self.timeout_seconds)} secs")
                        for i in range(math.ceil(self.timeout_seconds)):
                            time.sleep(1)

        return wrapper
