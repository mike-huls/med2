import logging
from logging.handlers import MemoryHandler

# Set up the main logger
logger = logging.getLogger("example_logger")
logger.setLevel(logging.DEBUG)

# Set up a stream handler to display logs (e.g., on console)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)  # Only INFO and above will be shown normally
logger.addHandler(stream_handler)

# Set up a memory handler to store DEBUG logs
memory_handler = MemoryHandler(capacity=100, target=stream_handler, flushLevel=logging.ERROR)
logger.addHandler(memory_handler)

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
