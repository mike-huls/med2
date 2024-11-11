import os
import random
import time
from typing import List, Dict

import psutil
import sqlalchemy as sa
from sqlalchemy import Column, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
import gc

Base = declarative_base()


class Client(Base):
    __tablename__ = "Clients"
    id = Column(sa.types.Integer, primary_key=True)
    name = Column(sa.types.String(50))
    email_address = Column(sa.types.String(50))


def send_email(message_list: List[Dict]) -> None:
    print(f"sent {len(message_list)} emails..")


def main(number: int):
    print("generating records...")
    sessionmaker = get_sessionmaker(record_count=number)
    print(f"generated {number} records")

    target_methods = [all_at_once, fetch_many_batches, fetch_many_walrus]
    target_methods = [fetch_many_walrus]

    for fn in target_methods:
        print("====start processing", fn.__name__)
        gc.collect()

        print("\n" + str(fn.__name__))
        strt = time.perf_counter()

        initial_memory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        avg_age: float = fn(session_maker=sessionmaker, batch_size=5_000)
        final_memory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

        print(f"{avg_age} time: {time.perf_counter() - strt:.2f}s --- {final_memory - initial_memory}")


def get_sessionmaker(record_count: int) -> sessionmaker:
    # 1. Create in-memory database
    db_engine: Engine = sa.create_engine(url=f"sqlite:///file:None?uri=true&mode=memory", echo=True)

    # 2. Make sure our table exists
    Base.metadata.create_all(bind=db_engine)

    # 3. Insert records
    session_maker = sa.orm.sessionmaker(db_engine)
    with session_maker() as con:
        for i in range(record_count):
            new_product = Client(id=i, name=f"name_{i}", email_address=f"email_address_{i}")
            con.add(new_product)
        con.commit()
    return session_maker


def all_at_once(session_maker: sessionmaker, batch_size: int) -> float:
    # 4. Load all records at once
    # strt = time.perf_counter()
    with session_maker() as con:
        all_records = con.execute(sa.select(Client)).fetchall()
        found_clients = [r.Client for r in all_records]

        email_messages = []
        for client in found_clients:
            msg = f"Hello {client.name}"

            email_messages.append({"msg": msg, "email": client.email_address})
            if len(email_messages) >= 500:
                send_email(email_messages)
                email_messages = []

    return 1


def fetch_many_batches(session_maker: sessionmaker, batch_size: int) -> float:
    # 5. Load records in batches of 25
    with session_maker() as con:
        result = con.execute(sa.select(Client))
        found_rows = result.fetchmany(batch_size)
        while found_rows:
            found_rows = result.fetchmany(batch_size)
            found_products = [r.Client for r in found_rows]
    return 1


def fetch_many_walrus(session_maker: sessionmaker, batch_size: int) -> float:
    # 6. Load records in batches of 25 with a rare walrus operator
    with session_maker() as con:
        t1 = time.perf_counter()
        result = con.execute(sa.select(Client))
        print(type(result))
        print("\t made select", time.perf_counter() - t1)
        t1 = time.perf_counter()
        while found_rows := result.fetchmany(size=batch_size):
            print("\t selected rows", time.perf_counter() - t1)
            found_clients = [r.Client for r in found_rows]
    return 1


if __name__ == "__main__":
    main(number=10_000)
