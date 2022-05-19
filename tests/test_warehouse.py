from datetime import datetime
import json
from app.routers import schemas
import pytest


@pytest.mark.parametrize("warehouse_name, warehouse_address, type, manager_id", [
    ("Warehouse Mars", "M88Z Mars ave Mars", "Spaceships", 1),
    ("Warehouse Juptiper", "J88Z Jupiter ave Jupiter", "Space food", 2),
    ("Warehouse Venus", "V88Z Venus ave Venus", "Space suits", 3)
])
def test_create_warehouse(client, test_warehouses, test_manager, warehouse_name, warehouse_address, type, manager_id):
    res = client.post("/warehouse/create", json={"warehouse_name": warehouse_name, "warehouse_address": warehouse_address, "type": type, "manager_id": manager_id })

    assert res.status_code == 201

def test_if_warehouse_name_is_empty(client):
    res = client.post("/warehouse/create", json={"warehouse_name": "", "warehouse_address": "123 tornoto ave", "type": "sports", "manager_id": 1})
    assert res.status_code == 422

def test_if_warehouse_address_is_empty(client):
    res = client.post("/warehouse/create", json={"warehouse_name": "London Warehosue", "warehouse_address": "", "type": "sports", "manager_id": 1})
    assert res.status_code == 422

def test_if_warehouse_type_is_empty(client):
    res = client.post("/warehouse/create", json={"warehouse_name": "London Warehouse", "warehouse_address": "123 tornoto ave", "type": "", "manager_id": 1})
    assert res.status_code == 422

def test_if_create_warehouse_with_manager_id_0(client):
    res = client.post("/warehouse/create", json={"warehouse_name": "London Warehouse", "warehouse_address": "123 tornoto ave", "type": "Tech", "manager_id": 0})
    assert res.status_code == 400
    

def test_get_all_warehouses(client, test_warehouses):
    res = client.get('/warehouse/all')
    assert res.status_code == 200

def test_get_warehouse_by_id(client, test_warehouses):
    res = client.get(f"/warehouse/1")
    assert res.status_code == 200 
    warehouse = schemas.WarehouseDisplay(**res.json())


def test_get_warehouse_with_non_exist_id(client, test_warehouses):
    res = client.get('/warehouse/8888')
    assert res.status_code == 404

def test_get_all_warehouses_with_searchbars(client):
    res = client.get("/warehouse/all?search_name=xscd&search_type=xsadv&search_address=cdsf&search_by_manager_id=5")
    assert res.status_code == 200

def test_delete_warehouse(client, test_warehouses):
    res = client.delete(f'warehouse/delete/2')
    assert res.status_code == 204

def test_delete_warehouse_non_exist(client, test_warehouses):
    res = client.delete('/warehouse/delete/88888')
    assert res.status_code == 404

def test_update_manager(client, test_warehouses, test_manager):
    data={
        "warehouse_name": "Warehouse100",
        "warehouse_address": "123, Talbot st",
        "type": "Tech",
        "manager_id":1
    }
    res = client.put(f'/warehouse/update/1', json=data)
    updated_warehouse = schemas.WarehouseBase(**res.json())
    assert res.status_code == 200
    assert updated_warehouse.warehouse_name == data["warehouse_name"]
    assert updated_warehouse.warehouse_address == data["warehouse_address"]
    assert updated_warehouse.type == data["type"]

def test_update_warehouse_non_exist(client, test_warehouses):
    data={
        "warehouse_name": "Warehouse100",
        "warehouse_address": "123, Talbot st",
        "type": "Tech",
        "manager_id":1
    }
    res = client.put('/warehouse/update/88888', json=data)
    assert res.status_code == 404



    
    
