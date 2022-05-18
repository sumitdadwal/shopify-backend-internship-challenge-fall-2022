from datetime import datetime
from routers import schemas
import pytest


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello Shopify, Go to /docs for all the end points.'
    assert res.status_code == 200



@pytest.mark.parametrize("first_name, last_name, manager_email, manager_phone", [
    ("John", "Doe", "johndoe@email.com", 8885554444),
    ("Jane", "Doe", "janedoe@email.com", 8885553333),
    ("Sumit", "Dadwal", "sumitdadwal1@gmail.com", 8885552222),
])
def test_create_managers(client, test_managers, first_name, last_name, manager_email, manager_phone):
    res = client.post("/manager/create", json={"first_name": first_name, "last_name": last_name, "manager_email": manager_email, "manager_phone": manager_phone})
    
    created_manager = schemas.ManagerBase(**res.json())
    assert res.status_code == 201
    assert created_manager.first_name == first_name
    assert created_manager.last_name == last_name
    assert created_manager.manager_email == manager_email
    assert created_manager.manager_phone == manager_phone

def test_if_first_and_last_name_are_empty(client):
    res = client.post("/manager/create", json={"first_name": "", "last_name": "", "manager_email": "test3@email.com", "manager_phone": 66447444888})

    assert res.status_code == 422


def test_get_all_managers(client, test_managers):
    res = client.get("/manager/all/")
    assert res.status_code == 200

def test_get_one_manager_not_exist(client, test_managers):
    res = client.get(f"/manager/8888")
    assert res.status_code == 404


def test_get_manager_by_id(client, test_managers):
    res  = client.get(f'/manager/{test_managers[0].manager_id}')
    manager = schemas.ManagerDisplay(**res.json())
    assert manager.manager_id == test_managers[0].manager_id
    assert manager.first_name == test_managers[0].first_name
    assert manager.last_name == test_managers[0].last_name
    assert manager.manager_email == test_managers[0].manager_email
    assert manager.manager_phone == test_managers[0].manager_phone

def test_delete_manager(client, test_managers):
    res = client.delete(f"manager/delete/{test_managers[0].manager_id}")
    assert res.status_code == 204

def test_delete_manager_non_exist(client, test_managers):
    res = client.delete(f"/manager/delete/88888")
    assert res.status_code == 404

def test_update_manager(client, test_managers):
    data = {
        "first_name": "Jon",
        "last_name": "Snow",
        "manager_email": "jonsnow@thewall.com",
        "manager_phone": 7775558888
    
    }
    res = client.put(f"/manager/update/{test_managers[0].manager_id}", json=data)
    updated_manager = schemas.ManagerBase(**res.json())
    assert res.status_code == 200
    assert updated_manager.first_name == data["first_name"]
    assert updated_manager.last_name == data["last_name"]
    assert updated_manager.manager_email == data["manager_email"]
    assert updated_manager.manager_phone == data["manager_phone"]

def test_update_manager_non_exist(client, test_managers):
    data = {
        "first_name": "Jon",
        "last_name": "Snow",
        "manager_email": "jonsnow@thewall.com",
        "manager_phone": 7775558888
    
    }
    

    res = client.put(f"manager/update/88888", json=data)

    assert res.status_code == 404    




