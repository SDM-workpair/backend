from fastapi.testclient import TestClient

from .matching import app  # Flask instance of the API

client = TestClient(app)


def test_matching_root():
    response = client.get("/")
    assert response.status_code == 200


def test_create_matching_event():
    response = client.post("/matching/create")
    assert response.status_code == 200
