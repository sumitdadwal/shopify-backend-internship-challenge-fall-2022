from xmlrpc.client import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    product_count = Column(Integer, nullable=False)
    product_description = Column(String, nullable=False)
    unit_price = Column(Integer, nullable=False)
    image_url = Column(String)
    image_url_type = Column(String)
    timestamp = Column(DateTime)
    warehouse_id = Column(Integer, ForeignKey('warehouse.warehouse_id', ondelete='CASCADE'))
    warehouse = relationship('Warehouse', back_populates='items')


class Warehouse(Base):
    __tablename__='warehouse'

    warehouse_id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String, nullable=False)
    warehouse_address = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    items = relationship('Product', back_populates='warehouse')

    manager_id = Column(Integer, ForeignKey('manager.manager_id'))
    manager = relationship('Manager', back_populates='warehouses')

class Manager(Base):
    __tablename__='manager'

    manager_id = Column(Integer, primary_key=True, index=True)
    manager_name = Column(String, nullable=False)
    manager_email = Column(String, unique=True, nullable=False)
    manager_phone = Column(Integer, nullable=False)
    
    warehouses = relationship('Warehouse', back_populates='manager')
