import logging
import queue
import time
from typing import Callable, List

from logging.handlers import QueueListener

from better_logger.dev.my_handlers import BatchHandler


def get_the_handler(logger: logging.Logger, callback: Callable) -> logging.Logger:
    log_queue = queue.Queue(maxsize=500)

    q_heartbeat = 1  # every 1 seconds

    # hh = QueueHandlerIgnoreLogsWhenFull(log_queue)
    # hh.setLevel(level=logging.ERROR)
    # logger.addHandler(hh)

    # 4. Start in seperate thread
    batch_handler = BatchHandler(callback=callback, flush_interval=1)
    print("created batch handler")

    queueListener = QueueListener(log_queue, batch_handler, q_heartbeat)
    print("created queue listener")
    queueListener.start()
    print("started queue listener")
    return logger, queueListener


if __name__ == "__main__":

    def fn_callback(records: List[logging.LogRecord]):
        print(records)
        print(type(records[0]))

    logger = logging.getLogger("TESTSTUFF")
    logger.setLevel(level=logging.DEBUG)
    # logger = get_the_handler(logger, callback=fn_callback)
    logger, listener = get_the_handler(logger, callback=fn_callback)
    print(logger)
    logger.debug("this is a debug message")
    logger.info("this is an info message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")

    time.sleep(1.1)

    listener.stop()
