import logging
import os
import sys
import uuid

import loguru
from loguru import logger

from envmanager.main import EnvManager

env = EnvManager(env=os.environ.get("ENV", 'dev'))



def main():

    # remove config for default handler (id == 0)
    logger.remove(0)
    # add new handler
    logger.add(
        sys.stderr,
        level="TRACE",
        # format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | <blue>{message}</blue> | {extra}",
        colorize=True,
        serialize=not env.is_dev,
        backtrace=True,
        diagnose=env.is_dev
    )
    logger.level("INFO", icon="ℹ️")



    logger.debug("pre-process")
    process_thing()
    logger.info("processed process")


    # logger.trace("A trace message.")
    # logger.debug("A debug message.")
    # logger.info("An info message.")
    # logger.success("A success message.")
    # logger.warning("A warning message.")
    # logger.error("An error message.")
    # logger.critical("A critical message.")



def process_thing():

    clogger = logger.bind(corr_id=uuid.uuid4(), prod_id="123")
    clogger.debug('process step 1')
    subfunction(logger=clogger)
    clogger.debug('process step 2')


def subfunction(logger):
    logger.debug('\tim a dub function')

    # try:
    #     1/0
    # except Exception as e:
    #     logger.exception('exception happened', )



if __name__ == "__main__":
    main()