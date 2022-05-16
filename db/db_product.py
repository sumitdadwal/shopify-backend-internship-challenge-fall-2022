from datetime import datetime
from itertools import product
from routers.schemas import ProductBase
from sqlalchemy.orm.session import Session
from db.models import Product
import datetime
from fastapi import HTTPException, status, Response

def new_product(db: Session, request: ProductBase):
    product = Product(
        product_name = request.product_name,
        product_count = request.product_count,
        product_description = request.product_description,
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        timestamp = datetime.datetime.now(),
        warehouse_id = request.warehouse_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

