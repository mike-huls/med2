import logging
from logging import handlers

from better_logger.internal_logger.loggers import logger_internal


class QueueHandlerIgnoreLogsWhenFull(handlers.QueueHandler):
    """When the queue is full and enqueue fails; it catches the error and ignores it."""

    def enqueue(self, record: logging.LogRecord):
        # print(f"debug, 9, {__file__} logrecord in handler {record}")
        try:
            super().enqueue(record=record)
        except Exception as e:
            logger_internal.info(msg=f"Error in QueueHandler: cannot enqueue: {e}")
