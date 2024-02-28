import json

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_root():
    test_response = {"message": "Hello World"}

    response = client.get("/")

    assert response.status_code == 200

    print(type(response.json))

    assert response.json() == test_response


def test_create_est():
    test_data = {
        "name": "Baghdad",
        "description": "Assasin's HQ",
        "location": "Ancient Baghdad City",
        "opening_hours": "09:00",
    }

    test_response = {
        "id": 1,
        "name": "Baghdad",
        "description": "Assasin's HQ",
        "location": "Ancient Baghdad City",
        "opening_hours": "09:00:00",
    }

    response = client.post("/inventory/establishments", json=test_data)

    assert response.status_code == 200

    assert response.json() == test_response
