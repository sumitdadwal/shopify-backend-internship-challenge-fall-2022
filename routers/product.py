from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status, UploadFile, File, Response
# from routers.schemas import ProductBase, ProductDisplay
from routers import schemas
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.db_product import new_product
from typing import List, Optional
from db.models import Product
import string
import random
import shutil
from datetime import datetime
import datetime


router = APIRouter(
    prefix='/product',
    tags=['product']
)

image_url_types = ['absolute', 'relative']

@router.post('/create', response_model=schemas.ProductDisplay)
def create_product(request: schemas.ProductBase, db: Session = Depends(get_db)):
    product = Product(
        product_name = request.product_name,
        product_count = request.product_count,
        product_description = request.product_description,
        unit_price = request.unit_price,
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        timestamp = datetime.datetime.now(),
        warehouse_id = request.warehouse_id
    )
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Parameter image_url_type can only take values 'absolute' or 'relative'.")
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get('/all', response_model=List[schemas.ProductDisplay])
def get_all_products(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search_name: Optional[str]='', search_description: Optional[str]='', search_count: Optional[int]='', search_warehouseID: Optional[int]='', search_unit_price: Optional[int]=''):
    all_products = db.query(Product).group_by(Product.product_id).filter(Product.product_name.contains(search_name)).filter(Product.product_description.contains(search_description)).filter(Product.product_count.contains(search_count)).filter(Product.warehouse_id.contains(search_warehouseID)).filter(Product.unit_price.contains(search_unit_price)).limit(limit).offset(skip).all()
    return all_products

@router.get('/{id}', response_model=schemas.ProductDisplay)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with Product ID {id} does not exist.')
    return product

@router.get('/warehouse/{warehouse_id}', response_model=List[schemas.ProductDisplay])
def get_product_by_warehouse_id(warehouse_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.warehouse_id == warehouse_id).all()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f'Product with Warehouse ID {warehouse_id} does not exist.')
    
    return product



@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{random_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

@router.put('/update/{id}', response_model=schemas.ProductDisplay)
def update_product(id: int, product: schemas.ProductBase, db: Session = Depends(get_db)):
    get_product = db.query(Product).filter(Product.product_id == id)
    updated_product = get_product.first()
    if updated_product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with ID {id} does not exist.')

    get_product.update(product.dict(), synchronize_session=False)
    db.commit()
    return get_product.first()

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    get_product = db.query(Product).filter(Product.product_id == id)
    product_delete = get_product.first()

    if product_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with ID {id} does not exist.')

    get_product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)