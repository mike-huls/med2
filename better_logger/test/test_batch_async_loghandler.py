import time
import unittest
from typing import List
from unittest.mock import MagicMock
import logging
from better_logger.dev.cgpt_handler import AsyncBufferHandler, LogRecord


class BufferedDBLogHandlerTest(unittest.TestCase):
    def setUp(self) -> None:
        """Setup the test environment before each test."""
        # Setup a mock callback function
        self.mock_callback = MagicMock()
        self.handler = AsyncBufferHandler(flush_interval=1, callback=self.mock_callback)

    def test_initialization(self) -> None:
        """Test handler initializes with correct flush interval and callback."""
        self.assertEqual(self.handler.flush_interval, 1)
        self.assertIsNotNone(self.handler.callback)

    def test_callback_invocation_with_log_records(self) -> None:
        """Test that the callback is invoked with the buffered log records."""
        # Create a log record and emit it, triggering the handler
        log_record = logging.LogRecord("test", logging.INFO, "", 0, "test message", None, None)
        self.handler.emit(log_record)

        # Wait for the flush interval to ensure the callback is invoked
        self.handler.flush_interval += 1  # Ensure there's enough time for flushing
        self.handler.flush()  # Manually trigger flush to ensure it's called

        # Verify the callback was called with a list of LogRecord objects
        self.mock_callback.assert_called_once()
        # Check that the first argument of the first call is a list of LogRecord
        args, _ = self.mock_callback.call_args
        self.assertIsInstance(args[0], list)
        self.assertIsInstance(args[0][0], LogRecord)

    def tearDown(self) -> None:
        """Clean up after each test."""
        self.handler.stop_flush_thread()
        del self.handler


class TestStuff(unittest.TestCase):
    def test_dignen(self):
        def fn_callback(logs: List[LogRecord]) -> None:
            print(logs)

        logger = logging.getLogger("my_application")
        logger.setLevel(logging.INFO)  # Set the desired log level

        # Create the handler instance
        handler = AsyncBufferHandler(flush_interval=1, callback=fn_callback, level=logging.ERROR)

        # Add the handler to the logger
        logger.addHandler(handler)

        # Now you can log messages, and they will be processed by your handler
        logger.info("This is a test log message.")

        logger.debug("This is a test debug log message.")
        logger.info("This is a test info log message.")
        logger.warning("This is a test warning log message.")
        logger.error("This is a test error log message.")
        logger.critical("This is a test critical log message.")

        for i in range(4):
            time.sleep(0.3)


if __name__ == "__main__":
    unittest.main()
