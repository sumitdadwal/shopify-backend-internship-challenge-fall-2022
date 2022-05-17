from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class ManagerBase(BaseModel):
    first_name: str
    last_name: str
    manager_email: EmailStr
    manager_phone: int

class ManagerDisplay(ManagerBase):
    manager_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class WarehouseBase(BaseModel):
    warehouse_name: str
    warehouse_address: str
    type: str
    manager_id: int

# for Warehouse Dispaly
class ManagerOut(ManagerDisplay):

    class Config:
        orm_mode = True

class WarehouseDisplay(BaseModel):
    warehouse_id: int
    warehouse_name: str
    warehouse_address: str
    type: str
    created_at: datetime
    manager: Optional[ManagerOut]
    

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    product_name: str
    product_description: str
    product_count: int
    unit_price: int
    image_url: str
    image_url_type: str
    warehouse_id: int

# for ProductDisplay
class WarehouseOut(BaseModel):
    warehouse_name: str
    warehouse_address: str
    type: str
    warehouse_id: int
    manager_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ProductDisplay(ProductBase):
    product_id: int
    created_at: datetime
    warehouse: Optional[WarehouseOut]

    class Config():
        orm_mode = True
