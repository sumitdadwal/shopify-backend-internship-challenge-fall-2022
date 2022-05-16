from datetime import datetime
from sqlite3 import Timestamp
from pydantic import BaseModel, EmailStr
from typing import List



class ManagerBase(BaseModel):
    manager_name: str
    manager_email: EmailStr

class ManagerDisplay(ManagerBase):
    manager_id: int
    class Config:
        orm_mode = True

class WarehouseBase(BaseModel):
    warehouse_name: str
    warehouse_address: str
    type: str
    manager_id: int

    

class WarehouseDisplay(WarehouseBase):
    warehouse_id: int
    
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

    class Config:
        orm_mode = True


class ProductDisplay(ProductBase):
    product_id: int
    timestamp: datetime
    warehouse_id: int
    warehouse: WarehouseOut

    class Config():
        orm_mode = True
