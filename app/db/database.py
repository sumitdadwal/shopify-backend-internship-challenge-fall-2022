from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///.shopify_api.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()

def get_db(): #dependancy #will help create session by calling it in each path operation function
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()