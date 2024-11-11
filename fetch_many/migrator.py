import os
import random
import time

import psutil
import sqlalchemy as sa
from sqlalchemy import Column, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
import gc

Base = declarative_base()


class Product(Base):
    __tablename__ = "Products"
    id = Column(sa.types.Integer, primary_key=True)
    name = Column(sa.types.String(50))
    price = Column(sa.types.Float)


def get_session_base_table(record_count: int) -> sessionmaker:
    # 1. Create in-memory database
    db_engine: Engine = sa.create_engine(url=f"sqlite:///file:None?uri=true&mode=memory", echo=False)

    # 2. Make sure our table exists
    Base.metadata.create_all(bind=db_engine)

    # 3. Insert records
    session_maker = sa.orm.sessionmaker(db_engine)
    with session_maker() as con:
        for i in range(record_count):
            new_product = Product(id=i, name="name_i", price=random.randint(1000, 6000) / 100)
            con.add(new_product)
        con.commit()
    return session_maker


def get_session_target_table() -> sessionmaker:
    db_engine: Engine = sa.create_engine(url=f"sqlite:///file:None?uri=true&mode=memory", echo=False)
    Base.metadata.create_all(bind=db_engine)
    session_maker = sa.orm.sessionmaker(db_engine)

    return session_maker


def main():
    sesmaker_base = get_session_base_table(record_count=1_000)
    sesmaker_target = get_session_target_table()

    print(id(sesmaker_base))
    print(id(sesmaker_target))

    with sesmaker_base() as con_base:
        with sesmaker_target() as con_target:
            result = con_base.execute(sa.select(Product))
            while found_rows := result.fetchmany(500):
                for r in found_rows:
                    con_target.add(r.Product)
                con_target.commit()

            res = con_target.execute(sa.select(Product))
            print(res.fetchall())

    # with sesmaker_base() as con_base:
    #     with sesmaker_target() as con_target:
    #         result = con_base.execute(sa.select(Product))
    #         while found_rows := result.fetchmany(500):
    #
    #             for r in found_rows:
    #                 con_target.add(r.Product)
    #             con_target.commit()
    #
    #         res = con_target.execute(sa.select(Product))
    #         print(res.fetchall())


if __name__ == "__main__":
    main()
