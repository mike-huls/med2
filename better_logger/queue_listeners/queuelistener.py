import atexit
import datetime
import logging
from queue import Empty

import time
from logging import handlers


from better_logger.queue_handlers.function_handler import FunctionHandler
from ..internal_logger.loggers import logger_internal


class QueueListenerBatch(handlers.QueueListener):
    _sentinel = None
    heartbeat_seconds: float

    def __init__(self, heartbeat_seconds: float = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.heartbeat_seconds = heartbeat_seconds
        atexit.register(self.__exit)
        self.start()

    def __exit(self):
        self._monitor(on_exit=True)

    def dequeue_batch(self, block: bool) -> [logging.LogRecord]:
        """Takes all items from a queue and returns them in an array"""
        queueContent: [logging.LogRecord] = []
        while self.queue.qsize() > 0:
            queueContent.append(self.queue.get(block=block))
        return queueContent

    # def handle(self, record:logging.LogRecord):
    #     """
    #     Handle a record.
    #
    #     This just loops through the handlers offering them the record
    #     to handle.
    #     """
    #     print("Handleleflasdlfadslfkj")
    #     record = self.prepare(record)
    #     for handler in self.handlers:
    #         if not self.respect_handler_level:
    #             process = True
    #         else:
    #             process = record.levelno >= handler.level
    #         if process:
    #             handler.handle(record)
    def handle_batch(self, records: [logging.LogRecord]):
        """
        Handle multiple records.

        This just loops through the handlers offering them the record
        to handle.
        """

        if len(records) == 0:
            return

        records = [self.prepare(record=rec) for rec in records]

        for handler in self.handlers:
            if self.respect_handler_level:
                records = [record.levelno >= handler.level for record in records]

            if isinstance(handler, FunctionHandler) or "handlebatch" in dir(handler):
                max_tries: int = 3
                current_try: int = 1
                while current_try <= max_tries:
                    try:
                        handler.emit(records=records)
                        break
                    except Exception as e:
                        handler._create_session()
                        logger_internal.debug(f"Attempting to recreate the session (try {current_try}/{max_tries}). Error: {e}")
                        if current_try >= max_tries:
                            raise e
                    finally:
                        current_try += 1
            else:
                for record in records:
                    handler.handle(record)

    def _monitor(self, on_exit: bool = False):
        """
        Monitor the queue for records, and ask the handler
        to deal with them.

        This method runs on a separate, internal thread.
        The thread will terminate if it sees a sentinel object in the queue.
        """

        q = self.queue
        has_task_done = hasattr(q, "task_done")
        while True:
            try:
                # 1. Get all records from the queue
                records: [logging.LogRecord] = self.dequeue_batch(block=True)

                # 2. First handle all non-sentinal records
                self.handle_batch(records=[rec for rec in records if (rec is not self._sentinel)])

                # 3. Break from the loop if we have a _sentinel or has_task_done
                break_while: bool = False
                for record in records:
                    if record is self._sentinel:
                        if has_task_done:
                            q.task_done()
                        break_while = True
                        break
                    # self.handle(record)   -->   (replaced by self.handle_batch
                    if has_task_done:
                        q.task_done()

                if break_while:
                    break
            except Empty:
                break
            except Exception as e:
                logger_internal.error(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Exception in sending log to HTTP endpoint: {e}")

            if on_exit:
                break
            time.sleep(self.heartbeat_seconds)
