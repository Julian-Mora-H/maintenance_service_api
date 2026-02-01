import os
import importlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client(tmp_path):
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    import app.core.config as config
    import app.db.session as session
    importlib.reload(config)
    importlib.reload(session)

    import app.main as main
    main.webbrowser.open = lambda *args, **kwargs: True

    class DummyTimer:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            pass

    main.threading.Timer = DummyTimer

    session.Base.metadata.drop_all(bind=session.engine)
    session.Base.metadata.create_all(bind=session.engine)

    return TestClient(main.app)


def test_create_and_list_categories(client):
    res = client.post("/router/categories/", json={"name": "Filtros"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Filtros"

    res = client.get("/router/categories/")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["name"] == "Filtros"


def test_create_and_list_items_with_category_left_join(client):
    cat = client.post("/router/categories/", json={"name": "Aceites"}).json()

    res = client.post(
        "/router/items/",
        json={
            "name": "Filtro de Aceite",
            "sku": "SKU-1001",
            "price": 25.5,
            "stock": 10,
            "category_id": cat["id"],
        },
    )
    assert res.status_code == 201

    res = client.get("/router/items/")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["category"]["name"] == "Aceites"


def test_patch_item_partial(client):
    res = client.post(
        "/router/items/",
        json={
            "name": "Filtro de Aire",
            "sku": "SKU-2002",
            "price": 50.0,
            "stock": 100,
            "category_id": None,
        },
    )
    item = res.json()

    res = client.patch(f"/router/items/{item['id']}", json={"price": 60.0})
    assert res.status_code == 200
    patched = res.json()
    assert patched["price"] == 60.0
    assert patched["stock"] == 100


def test_create_order_idempotent(client):
    item = client.post(
        "/router/items/",
        json={
            "name": "Filtro de Cabina",
            "sku": "SKU-3003",
            "price": 70.0,
            "stock": 5,
            "category_id": None,
        },
    ).json()

    payload = {
        "report": "Mantenimiento Preventivo",
        "items": [{"item_id": item["id"], "quantity": 2}],
        "request_id": None,
    }

    res1 = client.post(
        "/router/orders/",
        json=payload,
        headers={"Idempotency-Key": "abc123"},
    )
    assert res1.status_code == 201
    order1 = res1.json()

    res2 = client.post(
        "/router/orders/",
        json=payload,
        headers={"Idempotency-Key": "abc123"},
    )
    assert res2.status_code == 201
    order2 = res2.json()

    assert order1["id"] == order2["id"]

    res_list = client.get("/router/orders/")
    assert res_list.status_code == 200
    orders = res_list.json()
    assert len(orders) == 1
