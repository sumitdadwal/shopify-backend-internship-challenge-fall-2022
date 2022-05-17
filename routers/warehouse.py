from fastapi import APIRouter, Depends, status, HTTPException
from routers.schemas import WarehouseBase, WarehouseDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.models import Warehouse
from typing import List, Optional

router = APIRouter(
    prefix='/warehouse',
    tags=['warehouse']
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=WarehouseDisplay)
def create_warehouse(request: WarehouseBase, db: Session = Depends(get_db)):
    new_warehouse = Warehouse(
        warehouse_name = request.warehouse_name,
        warehouse_address = request.warehouse_address,
        type = request.type,
        manager_id = request.manager_id
    )
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse

@router.get('/all', response_model=List[WarehouseDisplay])
def get_all_warehouses(db: Session = Depends(get_db), search_name: Optional[str]='', search_type: Optional[str]='', search_address: Optional[str]='', search_by_manager_id: Optional[int]=''):
    warehouses = db.query(Warehouse).filter(Warehouse.warehouse_name.contains(search_name)).filter(Warehouse.warehouse_address.contains(search_address)).filter(Warehouse.type.contains(search_type)).filter(Warehouse.manager_id.contains(search_by_manager_id)).all()
    return warehouses

@router.get('/{id}', response_model=WarehouseDisplay)
def get_warehouse_by_id(id: int, db: Session = Depends(get_db)):
    warehouse = db.query(Warehouse).filter(Warehouse.warehouse_id == id).first()
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return warehouse


@router.put('/update/{id}', response_model=WarehouseDisplay)
def update_warehouse(id:int, request: WarehouseBase, db: Session = Depends(get_db)):
    get_warehouse = db.query(Warehouse).filter(Warehouse.warehouse_id == id)
    updated_warehosue = get_warehouse.first()

    if updated_warehosue == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Warehouse with ID {id} does not exist.')
    get_warehouse.update(request.dict(), synchronize_session=False)
    db.commit()
    return get_warehouse.first()


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(id: int, db: Session = Depends(get_db)):
    get_warehouse = db.query(Warehouse).filter(Warehouse.warehouse_id == id)
    deleted_warehouse = get_warehouse.first()

    if deleted_warehouse == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Warehouse with ID {id} does not exist.')
    get_warehouse.delete(synchronize_session=False)
    db.commit()