from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    category = Column(String(50), index=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
