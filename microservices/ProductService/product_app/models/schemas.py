from pydantic import BaseModel
from uuid import UUID


class ProductBase(BaseModel):
    name: str
    weight: float
    description: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str = None
    weight: float = None
    description: str = None


class Product(ProductBase):
    product_id: UUID

    class Config:
        orm_mode = True
