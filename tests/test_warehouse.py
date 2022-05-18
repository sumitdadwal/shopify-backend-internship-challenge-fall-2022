from datetime import datetime
from routers import schemas
import pytest

from tests.conftest import test_manager


@pytest.mark.parametrize("warehouse_name, warehouse_address, type, manager_id", [
    ("Warehouse Mars", "M88Z Mars ave Mars", "Spaceships", 1),
    ("Warehouse Juptiper", "J88Z Jupiter ave Jupiter", "Space food", 2),
    ("Warehouse Venus", "V88Z Venus ave Venus", "Space suits", 3)
])
def test_create_warehouse(client, test_warehouses, test_manager, warehouse_name, warehouse_address, type, manager_id):
    res = client.post("/warehouse/create", json={"warehouse_name": warehouse_name, "warehouse_address": warehouse_address, "type": type, "manager_id": manager_id })

    assert res.status_code == 201
    



def test_get_all_warehouses(client, test_warehouses):
    res = client.get('/warehouse/all')
    assert res.status_code == 200

def test_get_warehouse_by_id(client, test_warehouses):
    res = client.get(f"/warehouse/1")

    assert res.status_code == 200
    print(res.json())
    # warehouse = schemas.WarehouseDisplay(**res.json())
    # print(warehouse)
    # assert warehouse.warehouse_name == test_warehouses[0].warehouse_nmae
    # assert warehouse.warehouse_address == test_warehouses[0].warehouse_address
    # assert warehouse.type == test_warehouses[0].type

def test_get_warehouse_with_non_exist_id(client, test_warehouses):
    res = client.get('/warehouse/8888')
    assert res.status_code == 404
