import logging
import os
import sys
import structlog
import uuid



def main():
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(),
            # structlog.dev.set_exc_info,
            # structlog.processors.format_exc_info,

        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False
    )

    # Create logger
    logger = structlog.get_logger('tracker').bind(corr_id=uuid.uuid4(), prod_id="123")

    # logger.level("INFO", color="<blue>")


    logger.debug("A debug message.")
    logger.info("An info message.")
    logger.warning("A warning message.")
    logger.error("An error message.")
    logger.critical("A critical message.")


    logger.debug("pre-process")
    clogger = logger.bind(corr_id=uuid.uuid4(), prod_id="123")
    clogger.debug("about to process")
    process_thing(logger=logger)
    clogger.debug("processed process")


def process_thing(logger):
    logger.debug('process step 1')
    logger.debug('process step 2')

    try:
        1 / 0
    except Exception as e:
        logger.exception('exception happened', )


if __name__ == "__main__":

    main()