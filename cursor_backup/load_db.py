from random import randrange

import sqlalchemy as sa
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cursor_backup.tools.generation import generate_string
from cursor_backup.tools.loggingtools import logger
from cursor_backup.dtos import Product, Purchase, Customer, Base


def prep_db_small(db_engine_inmem: Engine):
    # Prepare in-memory database
    Base.metadata.create_all(db_engine_inmem)
    logger.debug(msg="IMEM - Created tables")

    # Step 6: Create a session
    with sessionmaker(bind=db_engine_inmem)() as ses_imem:
        # Step 7: Add some sample data
        product1 = Product(name="Laptop")
        product2 = Product(name="Smartphone")

        customer1 = Customer(name="Alice")
        customer2 = Customer(name="Bob")

        purchase1 = Purchase(product=product1, customer=customer1)
        purchase2 = Purchase(product=product2, customer=customer2)

        ses_imem.add_all([product1, product2, customer1, customer2, purchase1, purchase2])
        ses_imem.commit()
    logger.debug(msg="IMEM - Added sample data")


def prep_db_large(db_engine_inmem: Engine, n_customers: int):
    """1000 purchases, each with a product and customer"""

    N_PRODUCTS = int(n_customers / 10)
    N_PURCHASES = int(n_customers * 1.35)

    # Prepare in-memory database
    Base.metadata.create_all(db_engine_inmem)
    logger.debug(msg=f"IMEM - Created tables, inserting {n_customers} customers, {N_PRODUCTS} products and {N_PURCHASES} purchases")

    # Step 6: Create a session
    with sessionmaker(bind=db_engine_inmem)() as ses_imem:
        # Add Products
        ses_imem.add_all([Product(id=i, name=generate_string(size=5)) for i in range(N_PRODUCTS)])
        ses_imem.commit()

        # Add Customers
        ses_imem.add_all([Customer(id=i, name=generate_string(size=10)) for i in range(n_customers)])
        ses_imem.commit()

        # Add Purchases
        ses_imem.add_all([Purchase(product_id=randrange(N_PRODUCTS), customer_id=randrange(n_customers)) for _ in range(N_PURCHASES)])
        ses_imem.commit()

    logger.debug(msg="IMEM - Added sample data")
