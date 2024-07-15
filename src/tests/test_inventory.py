from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app
from src.config import settings


engine = create_engine(settings.TEST_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_est():
    test_data = {
        "name": "Alamut Castle",
        "description": "Assasin's HQ",
        "location": "Qazwin Plane",
        "opening_hours": "09:00:00",
    }

    test_response = {
        "id": 1,
        "name": "Alamut Castle",
        "description": "Assasin's HQ",
        "location": "Qazwin Plane",
        "opening_hours": "09:00:00",
    }

    response = client.post("/inventory/vendors", json=test_data)

    assert response.status_code == 200

    assert response.json() == test_response


def test_create_invalid_est():
    test_data = {
        "name": "Derinkuyu",
        "description": "Templar HQ",
        "location": "Cappadocia",
        "opening_hours": "ten",
    }

    response = client.post("/inventory/vendors", json=test_data)

    assert response.status_code == 422


def test_create_item():
    test_data = {
        "name": "Yatagan",
        "description": "Ottoman sword, imported from Istanbul",
        "price": 420,
        "quantity": 69,
    }

    test_response = {
        "name": "Yatagan",
        "description": "Ottoman sword, imported from Istanbul",
        "price": 420.0,
        "quantity": 69,
        "id": 1,
        "vendor_id": 1,
    }

    response = client.post("/inventory/vendors/1/items/", json=test_data)

    assert response.status_code == 200

    assert response.json() == test_response


def test_update_item():
    test_data = {
        "description": "Ottoman sword, imported from Istanbul(only 2 left)",
        "price": 210,
        "quantity": 2,
    }

    test_response = {
        "name": "Yatagan",
        "description": "Ottoman sword, imported from Istanbul(only 2 left)",
        "price": 210.0,
        "quantity": 2,
        "id": 1,
        "vendor_id": 1,
    }

    response = client.put("/inventory/items/1", json=test_data)

    print(response.json())

    assert response.status_code == 200

    assert response.json() == test_response


def test_update_item_invalid():
    test_data = {
        "description": "Ottoman sword, imported from Istanbul(only 2 left)",
        "price": 210,
        "quantity": "a lot of them",
    }

    response = client.post("/inventory/vendors/1/items/", json=test_data)

    assert response.status_code == 422


def test_create_invalid_item():
    test_data = {
        "description": "Ottoman sword, imported from Istanbul",
        "price": 420,
        "quantity": 69,
    }

    response = client.post("inventory/vendors/1/items/", json=test_data)

    assert response.status_code == 422


def test_delete_invalide_item():
    test_response = {"detail": "Item not found"}

    response = client.delete("inventory/vendors/32/")

    assert response.status_code == 404

    assert response.json() == test_response


def test_delete_item():
    response = client.delete("inventory/vendors/1/")

    assert response.status_code == 204
