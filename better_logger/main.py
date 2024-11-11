import logging
import queue
import time
from typing import Callable, List

from better_logger.queue_handlers.function_handler import FunctionHandler
from better_logger.queue_handlers.ignore_handler import QueueHandlerIgnoreLogsWhenFull
from better_logger.queue_listeners.queuelistener import QueueListenerBatch


# class BetterLogger:
#
#     def __init__(self, level):
#         self.logger = logging.getLogger("TESTSTUFF")
#         self.logger.setLevel(level=logging.INFO)
#         self.logger = setup_async_batch_logger(self.logger, callback=self.fn_callback)


def setup_async_batch_logger(target_logger: logging.Logger, callback: Callable, q_heartbeat_secs: float = 3, level: int = logging.NOTSET) -> logging.Logger:
    # 1. Create queue with a max size of 500 records
    log_queue = queue.Queue(maxsize=500)

    # 2. Add a handler that ignores logs when the queue is full
    target_logger.addHandler(QueueHandlerIgnoreLogsWhenFull(log_queue))

    # 3. Register a QueueListener that handles batches with a FunctionHandler with a callback
    QueueListenerBatch(q_heartbeat_secs, log_queue, FunctionHandler(callback=callback, level=level))

    return target_logger


if __name__ == "__main__":

    def fn_callback(records: List[logging.LogRecord]):
        print("found", len(records))
        print(type(records[0]))

    # def ddd(records:List[logging.LogRecord]):
    #     print('ddd', records)

    logger = logging.getLogger("TESTSTUFF")
    logger.setLevel(level=logging.INFO)
    logger = setup_async_batch_logger(logger, callback=fn_callback)

    # fn_handler = FunctionHandler(callback=ddd)
    # logger.addHandler(fn_handler)

    logger.debug("this is a debug message")
    logger.info("this is an info message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")

    time.sleep(1.1)
