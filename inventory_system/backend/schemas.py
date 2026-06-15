from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    quantity: int
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
