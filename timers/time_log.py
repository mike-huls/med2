import logging
import time
from contextlib import contextmanager


@contextmanager
def time_and_log(label: str, logger: logging.Logger, level: int = logging.DEBUG, slug: str = "TIME"):
    # Set the level: functions may be called within anot

    _slug = slug if (slug is not None) else ""

    strt = time.perf_counter()
    err = None
    duration: float

    try:
        yield
    except Exception as e:
        logger.warning(msg=f"Error executing function: {e}")
        err = e
    finally:
        duration = time.perf_counter() - strt

    status = "ERR" if err else "OK"
    log_level = logging.WARNING if err is not None else level
    msg = f"{_slug} ({status}) - {label} - {duration:.6f}s"

    logger.log(msg=msg, level=level)

    if err:
        raise err
