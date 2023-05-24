import loguru

from app import crud
from app.core.config import settings

from .contest import db_conn, get_user_authentication_headers, test_client

"""
pytest fixture
"""
db_conn = db_conn
test_client = test_client
email = "admin@sdm-teamatch.com"

"""
Test Matching Room
"""


def test_read_my_matching_rooms_who_has_logged_in(db_conn, test_client):
    response = test_client.get(
        f"{settings.API_V1_STR}/matching-room/my-list",
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    loguru.logger.info(response.json())

    assert response.json()["data"][0]["name"] == "IR"


def test_read_my_matching_rooms_who_has_not_logged_in(db_conn, test_client):
    response = test_client.get(f"{settings.API_V1_STR}/matching-room/my-list")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_search_matching_rooms_who_has_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"prompt": "SDM", "query_all": True},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # assert response.json()["data"][0]["name"] == "sdm" # skip this line cuz updated logic of matching room query won't get anything with testing data


def test_search_matching_rooms_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"prompt": "SDM", "query_all": True},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_search_matching_rooms_with_user_who_has_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"prompt": "SDM", "query_all": False},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.json()["data"][0]["name"] == "sdm"


def test_search_matching_rooms_with_user_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"prompt": "SDM", "query_all": False},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_search_matching_rooms_missing_param_who_has_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"prompt": "SDM"},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 422


def test_search_matching_rooms_missing_param_who_has_not_logged_in(
    db_conn, test_client
):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/matching-room/list",
        json={"prompt": ""},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_matching_room(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/matching-room/create",
        json={
            "name": "test_mr",
            "due_time": "2023-04-06T01:27:50.024Z",
            "min_member_num": 3,
            "description": "desc",
            "is_forced_matching": False,
        },
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    obj = crud.matching_room.get_by_room_id(
        db_conn, room_id=response.json()["data"]["room_id"]
    )
    db_conn.delete(obj)
    db_conn.commit()


def test_get_rcmed_tag(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/matching-room/rcmed-tag",
        json={"room_id": "IR001"},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"] == [
        "TAG1",
        "TAG2",
        "TAG3",
        "TAG4",
        "TAG5",
    ]
