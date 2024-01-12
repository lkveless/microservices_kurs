from pydantic import BaseModel
from uuid import UUID


class InventoryBase(BaseModel):
    product_name: str
    quantity_on_inventory: int
    current_price: float


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(InventoryBase):
    product_name: str = None
    quantity_on_inventory: int = None
    current_price: float = None


class Inventory(InventoryBase):
    product_id: UUID

    class Config:
        orm_mode = True
