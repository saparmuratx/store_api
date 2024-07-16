import string
import random

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

HEADERS = {"Authorization": "Bearer "}


def generate_username():
    characters = string.ascii_letters
    username = "".join(random.choice(characters) for _ in range(random.randint(5, 16)))
    return username


USERNAME = ""


def test_register():
    global USERNAME

    USERNAME = generate_username()

    test_data = {"username": USERNAME, "name": "Balancha", "password": "htmx"}

    test_response = {
        "username": USERNAME,
        "name": "Balancha",
        "created_date": "2024-07-15T09:43:14.625071",
    }

    response = client.post("/api/auth/register", json=test_data)
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert "username" in data and data["username"] == test_response["username"]

    assert "name" in data and data["name"] == test_response["name"]

    assert "created_date" in data


def test_login():
    test_data = {"username": USERNAME, "password": "htmx"}

    response = client.post("/api/auth/login", data=test_data)

    assert response.status_code == 200

    data = response.json()

    HEADERS["Authorization"] = "Bearer " + data["access_token"]


VENDOR_ID = 0


def test_create_vendor():
    global VENDOR_ID

    print(HEADERS)

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

    response = client.post("/api/inventory/vendors", json=test_data, headers=HEADERS)

    assert response.status_code == 200

    VENDOR_ID = response.json()["id"]
    test_response["id"] = VENDOR_ID
    test_response["user_id"] = response.json()["user_id"]

    assert response.json() == test_response


def test_create_invalid_vendor():
    test_data = {
        "name": "Derinkuyu",
        "description": "Templar HQ",
        "location": "Cappadocia",
        "opening_hours": "ten",
    }

    response = client.post("/api/inventory/vendors", json=test_data, headers=HEADERS)

    assert response.status_code == 422


ITEM_ID = 0


def test_create_item():
    global ITEM_ID

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
        "vendor_id": VENDOR_ID,
    }

    response = client.post(
        f"/api/inventory/vendors/{VENDOR_ID}/items/", json=test_data, headers=HEADERS
    )

    assert response.status_code == 200

    ITEM_ID = response.json()["id"]

    test_response["id"] = ITEM_ID

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
        "id": ITEM_ID,
        "vendor_id": VENDOR_ID,
    }

    response = client.put(
        f"/api/inventory/items/{ITEM_ID}/", json=test_data, headers=HEADERS
    )

    assert response.status_code == 200

    assert response.json() == test_response


def test_update_item_invalid():
    test_data = {
        "description": "Ottoman sword, imported from Istanbul(only 2 left)",
        "price": 210,
        "quantity": "a lot of them",
    }

    response = client.put(
        f"/api/inventory/items/{ITEM_ID}/", json=test_data, headers=HEADERS
    )

    assert response.status_code == 422


def test_create_invalid_item():
    test_data = {
        "description": "Ottoman sword, imported from Istanbul",
        "price": 420,
        "quantity": 69,
    }

    response = client.post(
        f"/api/inventory/vendors/{VENDOR_ID}/items/", json=test_data, headers=HEADERS
    )

    assert response.status_code == 422


def test_delete_invalid_item():
    test_response = {"detail": "Item not found"}

    response = client.delete("/api/inventory/items/42069/", headers=HEADERS)

    assert response.status_code == 404

    assert response.json() == test_response


def test_delete_invalid_vendor():
    test_response = {"detail": "Item not found"}

    response = client.delete("/api/inventory/vendors/42069/", headers=HEADERS)

    assert response.status_code == 404

    assert response.json() == test_response


def test_delete_item():
    response = client.delete(f"/api/inventory/items/{ITEM_ID}/", headers=HEADERS)

    assert response.status_code == 204

    response = client.get(f"/api/inventory/items/{ITEM_ID}", headers=HEADERS)

    assert response.status_code == 404


def test_delete_vendor():
    response = client.delete(f"/api/inventory/vendors/{VENDOR_ID}/", headers=HEADERS)

    assert response.status_code == 204

    response = client.get(f"/api/inventory/vendors/{VENDOR_ID}/", headers=HEADERS)

    assert response.status_code == 404
