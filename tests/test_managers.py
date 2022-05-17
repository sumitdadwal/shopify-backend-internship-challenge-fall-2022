from fastapi.testclient import TestClient
from app.main import app
from routers import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello Shopify, Go to /docs for all the end points.'
    assert res.status_code == 200

def test_create_manager():
    res = client.post("/manager/create", json={"manager_name": "test manager", "manager_email": "test@email.com", "manager_phone": 664444888})
    
    schemas.ManagerDisplay(**res.json())
    assert res.json().get("email") == "test@email.com"
    assert res.status_code == 201
