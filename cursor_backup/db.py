from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def imem_to_disk(engine_file: Engine, engine_imem: Engine):
    """Save the in-memory database to a disk"""

    # Access the raw SQLite connections
    in_memory_conn = engine_imem.raw_connection().driver_connection
    file_conn_raw = engine_file.raw_connection().driver_connection

    try:
        # Perform the backup from in-memory to file-based database
        in_memory_conn.backup(file_conn_raw)
    except Exception as e:
        print(f"error createin backup: {e}")
    # finally:
    #     Ensure connections are closed
    # in_memory_conn.close()
    # file_conn_raw.close()


def load_file_db_into_memory(file_db_path: Path) -> Engine:
    # Step 1: Create an in-memory SQLite database
    engine_in_memory: Engine = create_engine("sqlite:///:memory:")

    # Step 2: Create a file-based SQLite database connection
    engine_file_based: Engine = create_engine(f"sqlite:///{file_db_path}")

    # Step 3: Load data from the file-based database into the in-memory database
    file_conn_raw = engine_file_based.raw_connection().driver_connection
    memory_conn_raw = engine_in_memory.raw_connection().driver_connection

    try:
        file_conn_raw.backup(memory_conn_raw)
    except Exception as e:
        print(f"ERROR loading file into memory: {e}")
    finally:
        file_conn_raw.close()
        # memory_conn_raw.close()

    # Return the in-memory engine for further use
    return engine_in_memory
