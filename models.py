from sqlalchemy import Column, Integer, String

from database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sku = Column(String)
    group = Column(String)
    in_stock = Column(Integer)
    cost = Column(Integer)
