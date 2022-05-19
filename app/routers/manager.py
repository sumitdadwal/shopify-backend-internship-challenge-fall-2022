from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status, Response
from ..routers import schemas
from sqlalchemy.orm.session import Session
from ..db.database import get_db
from typing import List, Optional
from ..db.models import Manager
import datetime

router = APIRouter(
    prefix='/manager',
    tags=['manager']
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ManagerDisplay)
def create_manager(request: schemas.ManagerBase, db: Session = Depends(get_db)):
    new_manager = Manager(
        first_name = request.first_name,
        last_name = request.last_name,
        manager_email = request.manager_email,
        manager_phone = request.manager_phone,
        created_at = datetime.datetime.now()
    )

    if new_manager.first_name == "" and new_manager.last_name == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Cannot leave Manager Name Empty")

    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)
    return new_manager

@router.get('/{id}', response_model=schemas.ManagerDisplay)
def get_manager_by_id(id: int, db: Session = Depends(get_db)):
    manager = db.query(Manager).filter(Manager.manager_id == id).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Manager with id {id} not found.')
    
    return manager

@router.get('/all/', response_model=List[schemas.ManagerDisplay])
def get_all_managers(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search_first_name: Optional[str]= '', search_last_name: Optional[str]= '', search_email: Optional[str]= ''):
    managers = db.query(Manager).group_by(Manager.manager_id).filter(Manager.first_name.contains(search_first_name)).filter(Manager.last_name.contains(search_last_name)).filter(Manager.manager_email.contains(search_email)).limit(limit).offset(skip).all()
    return managers

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_manager(id: int, db: Session = Depends(get_db)):
    manager = db.query(Manager).filter(Manager.manager_id == id)
    deleted_manager = manager.first()

    if not deleted_manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Manager with id {id} does not exist.')
    manager.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put('/update/{id}', response_model=schemas.ManagerDisplay)
def update_manager(id: int, request: schemas.ManagerBase, db: Session = Depends(get_db)):
    manager = db.query(Manager).filter(Manager.manager_id == id)
    updated_manager = manager.first()

    if not updated_manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Manager with id {id} does not exist.')
    manager.update(request.dict(), synchronize_session=False)
    db.commit()

    return manager.first()
