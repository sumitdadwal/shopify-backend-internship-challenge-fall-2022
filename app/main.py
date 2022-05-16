from fastapi import FastAPI
from db import models
from db.database import engine
from routers import warehouse, product, manager
from fastapi.staticfiles import StaticFiles
# from auth import authentication
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(engine)


app = FastAPI()


app.include_router(warehouse.router)
app.include_router(product.router)
app.include_router(manager.router)


@app.get("/")
def root():
    return {"message": "Hello Shopify, Go to /docs for all the end points."}

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/images', StaticFiles(directory='images'), name='images')