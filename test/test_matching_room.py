from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app  # Flask instance of the API

client = TestClient(app)


def test_create_matching_room():
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/create",
        json={"name": "test_mr", "due_time": "2023-04-06T01:27:50.024Z",
              "min_member_num": 3, "description": "desc", "is_forced_matching": False}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'success'
    assert response.json()['data']['name'] == 'test_mr'


def test_get_my_matching_rooms():
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/my-list",
        json={"email": "admin@sdm-teamatch.com"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # assert response.json()['data'][0]['name'] == 'test_matching_room'


def test_get_my_matching_rooms_missing_param():
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/my-list",
        json={},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Fail to retrieve user's matching room. Missing parameter: email."
    )


def test_get_my_matching_rooms_user_not_found():
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/my-list",
        json={"email": "non-registered@gmail.com"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Fail to find user with this email."


def test_search_matching_rooms():
    response = client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"user_email": "", "prompt": "SDM", "query_all": True},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # assert response.json()['data'][0]['name'] == 'sdm'


def test_search_matching_rooms_with_user():
    response = client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"user_email": "admin@sdm-teamatch.com", "prompt": "", "query_all": False},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # assert response.json()['data'][0]['name'] == 'test_matching_room'


def test_search_matching_rooms_missing_param():
    response = client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"user_email": "", "prompt": "SDM", "query_all": False},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Fail to retrieve user's matching room. Missing parameter: email."
    )


def test_search_matching_rooms_user_not_found():
    response = client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={
            "user_email": "non-registered@gmail.com",
            "prompt": "",
            "query_all": False,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Fail to find user with this email."
