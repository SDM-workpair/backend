from fastapi.testclient import TestClient

from app.main import app  # Flask instance of the API

client = TestClient(app)


def test_read_main():
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_main_get_inffo():
    response = client.get("/api/basicinfo")
    assert response.status_code == 200


def test_main_get_items():
    response = client.get("/items/3?q=3")
    assert response.status_code == 200
    assert response.json() == {"item_id": 3, "q": "3"}
