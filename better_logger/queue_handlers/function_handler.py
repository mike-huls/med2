import logging
from logging import LogRecord
from typing import Callable, List, Union


class FunctionHandler(logging.Handler):
    """Register a function that gets called with the list of LogRecords"""

    callback: Callable

    def __init__(self, callback: Callable, level: int = logging.NOTSET):
        """
        :param callback: this function gets called with the list of LogRecords
        :type callback: Callable
        """

        self.callback = callback
        super().__init__(level=level)

    def emit(self, records: Union[LogRecord, List[LogRecord]]) -> None:
        """
        Overrides the emit method: call the callback function with the list of LogRecordd
        :param records: List of logrecords
        :type records: List[LogRecord]
        :return:
        """

        if isinstance(records, LogRecord):
            records = [records]
        records = [record for record in records if record.levelno >= self.level]

        self.callback(records)
