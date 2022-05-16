import email
from enum import unique
from xmlrpc.client import DateTime
import pydantic
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    product_count = Column(Integer)
    product_description = Column(String)
    unit_price = Column(Integer)
    image_url = Column(String)
    image_url_type = Column(String)
    timestamp = Column(DateTime)
    warehouse_id = Column(Integer, ForeignKey('warehouse.warehouse_id'))
    warehouse = relationship('Warehouse', back_populates='items')


# class Config:
#     arbitrary_types_allowed = True

# @pydantic.dataclasses.dataclass(config=Config)
class Warehouse(Base):
    __tablename__='warehouse'

    warehouse_id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String)
    warehouse_address = Column(String, unique=True)
    type = Column(String)
    items = relationship('Product', back_populates='warehouse')

    manager_id = Column(Integer, ForeignKey('manager.manager_id'))
    manager = relationship('Manager', back_populates='warehouse')

class Manager(Base):
    __tablename__='manager'

    manager_id = Column(Integer, primary_key=True, index=True)
    manager_name = Column(String)
    manager_email = Column(String, unique=True)
    warehouse = relationship('Warehouse', back_populates='manager')
