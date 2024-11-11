import logging
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cursor_backup.db import imem_to_disk, load_file_db_into_memory
from cursor_backup.dtos import Product, Purchase
from cursor_backup.load_db import prep_db_large
from timers.time_log import time_and_log
from cursor_backup.tools.loggingtools import logger


def main():
    ROOT_DIR = Path(__file__).parent
    DB_PATH = Path(ROOT_DIR, "db_backup.db")

    # Create the database engines
    engine_file_based = create_engine(f"sqlite:///{DB_PATH}")
    engine_in_memory = create_engine("sqlite:///:memory:")

    # Remove file db if exists
    if DB_PATH.exists():
        DB_PATH.unlink()

    # prepare the database - crate tables + content
    with time_and_log(label="create_dataset", logger=logger, level=logging.INFO):
        prep_db_large(db_engine_inmem=engine_in_memory, n_customers=10_000)

    # Backup the data to a file
    with time_and_log(label="imem->file", logger=logger, level=logging.INFO):
        imem_to_disk(engine_file=engine_file_based, engine_imem=engine_in_memory)

    # Close all databases
    engine_in_memory.dispose()
    engine_file_based.dispose()

    # Create new in-memory database and load the file-data into it
    with time_and_log(label="file->imem", logger=logger, level=logging.INFO):
        new_imem_engine: Engine = load_file_db_into_memory(file_db_path=DB_PATH)

    # Query the data to verify it was loaded correctly
    with sessionmaker(bind=new_imem_engine)() as ses_imem:
        purchase: Optional[Purchase] = ses_imem.query(Purchase).first()
        if purchase is not None:
            logger.debug(msg=f"Purchase: {purchase}")
            logger.debug(msg=f"Purchase: {purchase.customer} {purchase.product}")


if __name__ == "__main__":
    main()
