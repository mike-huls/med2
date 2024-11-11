import sys

from loguru import logger
import logging
from logging.handlers import MemoryHandler

# Set up a standard logging StreamHandler
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.INFO)  # Only output INFO and above by default

logger.remove(0)        # removes default console handler
logger.add(
    sink=sys.stderr,
    level="TRACE",
    format="{level.icon}<green>{time:HH:MM:SS} @{module}:{function}:{level.no}</green>  <level>{message}</level> \t <yellow>extra={extra}</yellow>",
    serialize=False,
    backtrace=True,
    diagnose=True
)

# Set up a MemoryHandler to buffer DEBUG logs
# memory_handler = MemoryHandler(capacity=100, target=, flushLevel=logging.ERROR)

# Link Loguru to the standard logging handler
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Intercept standard logging messages and pass them to Loguru
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0)

# Function to add the MemoryHandler to Loguru
def add_memory_handler():
    # Set up standard logging configuration with MemoryHandler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(memory_handler)

    # Intercept Loguru logs and send them to the MemoryHandler
    logger.add(lambda msg: root_logger.handle(logging.makeLogRecord({'msg': msg, 'levelno': logging.DEBUG})), level="DEBUG")


#
class MemoryHandler:
    def __init__(self, capacity, target_sink):
        self.capacity = capacity
        self.target_sink = target_sink
        self.buffer = []

    def write(self, message):
        self.buffer.append(message)
        if len(self.buffer) >= self.capacity:
            self.flush()

    def flush(self):
        for message in self.buffer:
            self.target_sink.write(message)
        self.buffer.clear()

    def close(self):
        self.flush()

# Example usage
import sys

# Create a memory handler with capacity 5 that flushes to sys.stdout
memory_handler = MemoryHandler(capacity=5, target_sink=sys.stdout)

#
# Add the MemoryHandler to Loguru
# add_memory_handler()
# logger.remove(0)
logger.add(sink=memory_handler)
# Sample function with logging
def divide_500(number:int):
    logger.debug(f"Start dividing 500 by {number}")

    if isinstance(number, str):
        raise ValueError(f"Number is a {type(number)}; should be a string")

    return 500 / number

def main():

    for value in [1, 3, 'not a number']:
        try:
            logger.info(f"--->Processing [{value}]..")
            divide_500(value)
            logger.info(f"Processed {value}")
        except Exception as e:
            # Log the exception
            logger.error("An exception occurred")
            # Flush memory handler to print all DEBUG logs
            memory_handler.flush()

if __name__ == "__main__":
    main()

def main():

    for value in [1, 3, 'not a number']:
        try:
            logger.info(f"--->Processing [{value}]..")
            divide_500(value)
            logger.info(f"Processed {value}")
        except Exception as e:
            # Log the exception
            logger.error("An exception occurred")
            # Flush memory handler to print all DEBUG logs
            memory_handler.flush()



