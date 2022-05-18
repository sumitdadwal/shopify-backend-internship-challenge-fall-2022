from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db.database import get_db
from db.database import Base
import pytest
from db import models
from datetime import datetime

SQLALCHEMY_DATABASE_URL = 'sqlite:///.shopify_api_test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                    connect_args={'check_same_thread': False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

@pytest.fixture()
def session():
    #drop all tables ones tests runs again. to avoid duplicate data errors
    Base.metadata.drop_all(engine)
    #create new tables before our test runs
    Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db(): #dependancy #will help create session by calling it in each path operation function
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    #run tests
    yield TestClient(app)

@pytest.fixture
def test_managers(session):
    manager_data = [{
        "first_name": "test",
        "last_name": "manager",
        "manager_email": "test@email.com",
        "manager_phone": 666555888,
        "created_at": datetime.now()
    },
    {
        "first_name": "test2",
        "last_name": "manager",
        "manager_email": "test2@email.com",
        "manager_phone": 6688885888,
        "created_at": datetime.now()
    },
    {
        "first_name": "test3",
        "last_name": "manager",
        "manager_email": "test3@email.com",
        "manager_phone": 66655588888,
        "created_at": datetime.now()
    }]

    def create_manager_model(manager):
        return models.Manager(**manager)

    manager_map = map(create_manager_model, manager_data)
    managers = list(manager_map)

    session.add_all(managers)

    # session.add_all([models.Manager(first_name="test", last_name="manager", manager_email="testmanager@email.com", manager_phone=5558884444, created_at= datetime.now()),
    #                 models.Manager(first_name="test2", last_name="manager", manager_email="testmanager2@email.com", manager_phone=55584884444, created_at= datetime.now()),
    #                 models.Manager(first_name="test3", last_name="manager", manager_email="testmanage3r@email.com", manager_phone=5558884444, created_at= datetime.now())])
    session.commit()
    managers = session.query(models.Manager).all()
    return managers



@pytest.fixture
def test_warehouses(session):
    warehouse_data = [{
        "warehouse_name": "Warehouse1",
        "warehouse_address": "123 king st",
        "type": "Electronics",
        "manager_id": 1,
        "created_at": datetime.now()
    },
    {
        "warehouse_name": "Warehouse2",
        "warehouse_address": "123 Queen st",
        "type": "Clothing",
        "manager_id": 2,
        "created_at": datetime.now()
    },
    {
        "warehouse_name": "Warehouse3",
        "warehouse_address": "123 Bay st",
        "type": "Computer Parts",
        "manager_id": 3,
        "created_at": datetime.now()
    }]

    def create_warehouse_model(warehouse):
        return models.Warehouse(**warehouse)

    warehouse_map = map(create_warehouse_model, warehouse_data)
    warehouses = list(warehouse_map)

    session.add_all(warehouses)

    # session.add_all([models.Manager(first_name="test", last_name="manager", manager_email="testmanager@email.com", manager_phone=5558884444, created_at= datetime.now()),
    #                 models.Manager(first_name="test2", last_name="manager", manager_email="testmanager2@email.com", manager_phone=55584884444, created_at= datetime.now()),
    #                 models.Manager(first_name="test3", last_name="manager", manager_email="testmanage3r@email.com", manager_phone=5558884444, created_at= datetime.now())])
    session.commit()
    warehouses = session.query(models.Warehouse).all()
    return 

@pytest.fixture
def test_products(session):
    product_data = [{
        "product_name": "TestProduct1",
        "product_description": "This Product is for testing purposes.",
        "product_count": 100,
        "unit_price": 50,
        "image_url": "https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8Zm9jdXN8ZW58MHx8MHx8&w=1000&q=80",
        "image_url_type": "absolute",
        "warehouse_id": 1,
        "created_at": datetime.now()
    },
    {
        "product_name": "TestProduct2",
        "product_description": "This the second Product is for testing purposes.",
        "product_count": 150,
        "unit_price": 80,
        "image_url": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg",
        "image_url_type": "absolute",
        "warehouse_id": 2,
        "created_at": datetime.now()
    },
    {
        "product_name": "TestProduct3",
        "product_description": "This the third Product is for testing purposes.",
        "product_count": 200,
        "unit_price": 100,
        "image_url": "https://helpx.adobe.com/content/dam/help/en/photoshop/using/convert-color-image-black-white/jcr_content/main-pars/before_and_after/image-before/Landscape-Color.jpg",
        "image_url_type": "absolute",
        "warehouse_id": 1,
        "created_at": datetime.now()
    }]

    def create_product_model(product):
        return models.Product(**product)

    product_map = map(create_product_model, product_data)
    products = list(product_map)

    session.add_all(products)
    session.commit()
    products = session.query(models.Product).all()
    return products





    

@pytest.fixture
def test_manager(client):
    manager_data = {"first_name": "tim", "last_name": "dillon", "manager_email":"emailfortests@email.com", 
                    "manager_phone": 8887774444}
    res = client.post("/manager/create", json=manager_data)

    assert res.status_code == 201

    new_manager = res.json()
    return new_manager
  
