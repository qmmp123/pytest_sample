from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    sku: str
    group: str
    in_stock: int
    cost: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
