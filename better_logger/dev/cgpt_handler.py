import logging
import threading
import time
from typing import List, Callable, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession

Base = declarative_base()


class LogRecord(Base):
    __tablename__ = "log_records"
    id = Column(Integer, primary_key=True)
    level = Column(String(50))
    message = Column(String(256))

    def __init__(self, level: str, message: str) -> None:
        self.level = level
        self.message = message


# Assuming DATABASE_URI and Base.metadata.create_all(engine) are defined elsewhere


class AsyncBufferHandler(logging.Handler):
    def __init__(self, flush_interval: int = 5, level: int = logging.NOTSET, callback: Optional[Callable[[List[LogRecord]], None]] = None) -> None:
        super().__init__(level)
        self.flush_interval = flush_interval
        self.buffer: List[LogRecord] = []
        self.lock = threading.Lock()
        self.callback = callback
        self.stop_event = threading.Event()  # Signal for stopping the thread
        self.flush_thread = threading.Thread(target=self.flush_periodically)
        self.flush_thread.daemon = True
        self.flush_thread.start()

    def emit(self, record: logging.LogRecord) -> None:
        print(record, "logrecord")
        log_entry = LogRecord(level=record.levelname, message=record.getMessage())
        with self.lock:
            self.buffer.append(log_entry)

    def flush_periodically(self) -> None:
        while not self.stop_event.wait(self.flush_interval):  # Wait for stop signal or timeout
            self.flush()

    def flush(self) -> None:
        with self.lock:
            if self.buffer and self.callback:
                self.callback(self.buffer)
                self.buffer = []

    def stop_flush_thread(self) -> None:
        """Signal the flush thread to stop and wait for it to finish."""
        self.stop_event.set()
        self.flush_thread.join()
