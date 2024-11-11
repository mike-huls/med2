import logging
from logging.handlers import MemoryHandler


# logging.basicConfig(
#     level=logging.DEBUG,
#     datefmt="%H:%M:%S",
#     format="%(levelname)-6s ⏱️%(asctime)s  📍%(funcName)-17s:%(lineno)-2s  💌%(message)s",
#     # format="%(levelname)-6s ⏱️%(asctime)s  📍%(funcName)-17s:%(lineno)-2s  🔎%(correlation_id)s  💌%(message)s",
# )
formatter = logging.Formatter(
    fmt="%(levelname)-7s ⏱️%(asctime)s  📍%(funcName)12s:%(lineno)-2s  💌%(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("example_logger")
logger.setLevel(level=logging.DEBUG)

# Set up a stream handler to display logs (e.g., on console) and add
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # Only INFO and above will be shown normally
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Set up a memory handler to store DEBUG logs
memory_handler = MemoryHandler(capacity=100, target=stream_handler, flushLevel=logging.ERROR)
memory_handler.setFormatter(formatter)
logger.addHandler(memory_handler)

# Sample function with logging
def divide(a, b):
    logger.debug(f"Dividing [{a}] by [{b}]")
    return a / b

# ⚠️❗❌
def main():
    # Set up the main logger

    for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 'not a number', 0]:
        try:
            logger.debug(f"start dividing..")
            res = divide(a=10, b=value)
        except Exception as e:
            logger.error(f"❌An exception occurred: {e}")
        finally:
            memory_handler.buffer.clear()


if __name__ == "__main__":
    main()
