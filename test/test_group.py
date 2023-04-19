from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app  # Flask instance of the API

client = TestClient(app)


def test_get_my_groups():
    response = client.post(
        f"{settings.API_V1_STR}/group/my-list",
        json={"email": "admin@sdm-teamatch.com"},
    )
    assert response.status_code == 200
    # assert response.json()['data'][0]['name'] == 'test_matching_room-group001'


def test_get_my_groups_missing_param():
    response = client.post(
        f"{settings.API_V1_STR}/group/my-list",
        json={},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Fail to retrieve user's group. Missing parameter: email."
    )


def test_get_my_groups_user_not_found():
    response = client.post(
        f"{settings.API_V1_STR}/group/my-list",
        json={"email": "non-registered@gmail.com"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Fail to find user with this email."


def test_search_groups():
    response = client.post(
        f"{settings.API_V1_STR}/search/group/list",
        json={"user_email": "admin@sdm-teamatch.com", "prompt": "test"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # assert response.json()['data'][0]['name'] == 'test_matching_room-group001'


def test_search_groups_missing_param():
    response = client.post(
        f"{settings.API_V1_STR}/search/group/list",
        json={"user_email": "", "prompt": "test"},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Fail to retrieve user's group. Missing parameter: email."
    )


def test_search_groups_user_not_found():
    response = client.post(
        f"{settings.API_V1_STR}/search/group/list",
        json={"user_email": "non-registered@gmail.com", "prompt": "test"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Fail to find user with this email."
