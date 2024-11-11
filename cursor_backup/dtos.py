from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from cursor_backup.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship with Purchase
    purchases = relationship("Purchase", back_populates="product")

    def __str__(self):
        return f"<Product {self.id} - {self.name} (bought {len(self.purchases)} times)>"


# Step 3: Define the Customer model
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship with Purchase
    purchases = relationship("Purchase", back_populates="customer")

    def __str__(self):
        return f"<Customer {self.id} - {self.name} ({len(self.purchases)} purchases)>"


# Step 4: Define the Purchase model
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Relationships to Product and Customer
    product = relationship("Product", back_populates="purchases")
    customer = relationship("Customer", back_populates="purchases")

    def __str__(self):
        return f"<Purchase of {self.product} by {self.customer}>"
