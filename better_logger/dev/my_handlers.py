import copy
import getpass
import logging
import threading
import time
from typing import Callable, List


# import requests
# from requests.adapters import HTTPAdapter
# from urllib3 import Retry
#


class BatchHandler(logging.Handler):
    """Overrides the 'emit' method on the logging.Handler class
    Posts the message to an http endpoint
    """

    callback: Callable

    buffer: List[logging.LogRecord]
    lock: threading.Lock
    flush_thread: threading.Thread
    flush_interval: float
    stop_event: threading.Event

    def __init__(self, callback: Callable, flush_interval: int = 5) -> None:
        """Initializes the custom http handler
        Parameters:
            url (str): The URL that the logs will be sent to
            token (str): The Authorization token being used
        """
        print("1ogo")
        super().__init__()
        print("gogo")

        self.callback = callback

        self.flush_interval = flush_interval
        self.buffer: List[logging.LogRecord] = []
        self.lock = threading.Lock()
        self.callback = callback
        self.stop_event = threading.Event()  # Signal for stopping the thread
        self.flush_thread = threading.Thread(target=self.flush_periodically)
        self.flush_thread.daemon = True
        print("starting thread")
        self.flush_thread.start()
        print("thread started")

    def emit(self, record: logging.LogRecord) -> None:
        print(record, "logrecord")
        # log_entry = logging.LogRecord(level=record.levelname, message=record.getMessage())
        with self.lock:
            self.buffer.append(record)

    def flush_periodically(self) -> None:
        while not self.stop_event.wait(self.flush_interval):  # Wait for stop signal or timeout
            self.flush()

    def flush(self) -> None:
        with self.lock:
            # todo check if callback exists?
            if len(self.buffer) > 0 and self.callback:
                self.callback(self.buffer)
                self.buffer = []

    def stop_flush_thread(self) -> None:
        """Signal the flush thread to stop and wait for it to finish."""
        self.stop_event.set()
        self.flush_thread.join()


if __name__ == "__main__":

    def fn_callback(records: List[logging.LogRecord]):
        print("callback")
        print(records)
        print(type(records[0]))

    logger = logging.getLogger("TESTSTUFF")
    hndlr = BatchHandler(callback=fn_callback, flush_interval=1)
    logger.addHandler(hndlr)

    logger.debug("this is a debug message")
    logger.info("this is an info message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
    logger.critical("this is a critical message")

    time.sleep(1.1)
