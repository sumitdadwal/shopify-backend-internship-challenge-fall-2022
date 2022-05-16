from fastapi import HTTPException, status
from routers.schemas import WarehouseBase
from sqlalchemy.orm.session import Session
from db.models import Warehouse

def new_warehouse(db: Session, request: WarehouseBase):
    new_warehouse = Warehouse(
        warehouse_name=request.warehouse_name,
        warehouse_address=request.warehouse_address
    )

    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse

    