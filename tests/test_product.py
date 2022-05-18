from itertools import product
from math import prod
from routers import schemas
import pytest

from tests.conftest import test_managers


@pytest.mark.parametrize("product_name, product_description, product_count, unit_price, image_url, image_url_type, warehouse_id", [
    ("AwesomeProduct", "This is an awesome product", 100, 50, "https://image.com", "absolute", 1),
    ("AwesomeProduct2", "This is the second awesome product", 100, 50, "https://image.com", "absolute", 2),
    ("AwesomeProduct3", "This is the third awesome product", 100, 50, "https://image.com", "absolute", 3)
])
def test_create_products(client, test_products, product_name, product_description, product_count, unit_price, image_url, image_url_type, warehouse_id):
    res = client.post("/product/create", json={"product_name": product_name, "product_description": product_description, "product_count": product_count, "unit_price": unit_price, "image_url": image_url, "image_url_type": image_url_type, "warehouse_id": warehouse_id})

    created_products = schemas.ProductBase(**res.json())
    assert created_products.product_name == product_name
    assert created_products.product_description == product_description
    assert created_products.product_count == product_count
    assert created_products.unit_price == unit_price
    assert created_products.image_url == image_url
    assert created_products.image_url_type == image_url_type
    assert created_products.warehouse_id == warehouse_id

def test_if_product_name_is_empty(client):
    res = client.post("/product/create", json={"product_name": "", "product_description": "This is an awesome product", "product_count": 100, "unit_price": 50, "image_url": "https://image.com", "image_url_type" : "absolute", "warehouse_id": 1})
    assert res.status_code == 422

def test_if_product_descripion_is_empty(client):
    res = client.post("/product/create", json={"product_name": "Project Name", "product_description": "", "product_count": 100, "unit_price": 50, "image_url": "https://image.com", "image_url_type" : "absolute", "warehouse_id": 1})
    assert res.status_code == 422

def test_for_wrong_image_url_type(client):
    res = client.post("/product/create", json={"product_name": "Product Name", "product_description": "This is an awesome product", "product_count": 100, "unit_price": 50, "image_url": "https://image.com", "image_url_type" : "completeUrl", "warehouse_id": 1})
    assert res.status_code == 422

def test_get_all_products(client, test_products):
    res = client.get("/product/all")
    assert res.status_code == 200

def test_get_product_by_id(client, test_products):
    res = client.get(f"/product/{test_products[0].product_id}")
    product = schemas.ProductDisplay(**res.json())
    assert product.product_id == test_products[0].product_id
    assert product.product_name == test_products[0].product_name
    assert product.product_description == test_products[0].product_description
    assert product.product_count == test_products[0].product_count
    assert product.unit_price == test_products[0].unit_price
    assert product.image_url == test_products[0].image_url
    assert product.image_url_type == test_products[0].image_url_type
    assert product.warehouse_id == test_products[0].warehouse_id
    assert product.warehouse == test_products[0].warehouse

def test_get_product_by_id_non_exist(client, test_products):
    res = client.get(f'product/8888')
    assert res.status_code == 404

def test_get_product_by_warehouse_id(client, test_products):
    res = client.get(f"/product/{test_products[0].warehouse_id}")
    product = schemas.ProductDisplay(**res.json())
    assert product.product_id == test_products[0].product_id
    assert product.product_name == test_products[0].product_name
    assert product.product_description == test_products[0].product_description
    assert product.product_count == test_products[0].product_count
    assert product.unit_price == test_products[0].unit_price
    assert product.image_url == test_products[0].image_url
    assert product.image_url_type == test_products[0].image_url_type
    assert product.warehouse_id == test_products[0].warehouse_id
    assert product.warehouse == test_products[0].warehouse 


def test_get_all_products_with_limit(client):
    res = client.get("/product/all?limit=2&skip=1")
    assert res.status_code == 200

def test_get_all_products_with_search(client):
    res = client.get("/product/all?limit=1&skip=0&search_name=dc&search_description=xs&search_warehouseID=500&search_unit_price=55")
    assert res.status_code == 200




