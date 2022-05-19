from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import get_db
from app.db.database import Base
import pytest

SQLALCHEMY_DATABASE_URL = 'sqlite:///.shopify_api_test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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