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
def test_warehouses(test_managers, session):
    warehouse_data = [{
        "warehouse_name": "Warehouse1",
        "warehouse_address": "123 king st",
        "type": "Electronics",
        "manager_id": test_managers[0].manager_id,
        "created_at": datetime.now()
    },
    {
        "warehouse_name": "Warehouse2",
        "warehouse_address": "123 Queen st",
        "type": "Clothing",
        "manager_id": test_managers[0].manager_id,
        "created_at": datetime.now()
    },
    {
        "warehouse_name": "Warehouse3",
        "warehouse_address": "123 Bay st",
        "type": "Computer Parts",
        "manager_id": test_managers[2].manager_id,
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
def test_manager(client):
    manager_data = {"first_name": "tim", "last_name": "dillon", "manager_email":"emailfortests@email.com", 
                    "manager_phone": 8887774444}
    res = client.post("/manager/create", json=manager_data)

    assert res.status_code == 201

    new_manager = res.json()
    return new_manager
  
