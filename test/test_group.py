import json
import unittest
import uuid
from base64 import b64encode
from datetime import datetime, timedelta
from unittest import mock

from fastapi.encoders import jsonable_encoder
from itsdangerous import TimestampSigner

from app import crud
from app.core import security
from app.core.config import settings
from app.database.session import db_session
from app.main import app  # Flask instance of the API

from .contest import db_conn, get_user_authentication_headers, test_client

"""
pytest fixture
"""
db_conn = db_conn
test_client = test_client
email = "admin@sdm-teamatch.com"

"""
Test Group
"""


def test_read_my_groups_who_has_logged_in(db_conn, test_client):
    response = test_client.get(
        f"{settings.API_V1_STR}/group/my-list",
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"][0]["group_id"] == "test_matching_room-group1"


def test_read_my_groups_who_has_not_logged_in(db_conn, test_client):
    response = test_client.get(f"{settings.API_V1_STR}/group/my-list")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_search_groups_who_has_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/group/list",
        json={"prompt": "test"},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"][0]["group_id"] == "test_matching_room-group1"


def test_search_groups_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/search/group/list", json={"prompt": "test"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_search_groups_missing_param_who_has_logged_in(db_conn, test_client):

    response = test_client.post(
        f"{settings.API_V1_STR}/search/group/list",
        json={},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 422


def test_search_groups_missing_param_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(f"{settings.API_V1_STR}/search/group/list", json={})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_read_group_members_who_has_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/group/members",
        json={"group_id": "test_matching_room-group1"},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()[
        "data"][0]["name"] == "admin"


def test_read_group_members_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/group/members", json={"group_id": ""}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_read_group_members_empty_group_id_who_has__logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/group/members",
        json={"group_id": ""},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Fail to get group members. Missing parameter: group_id."
    )


def test_read_group_members_empty_group_id_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/group/members", json={"group_id": ""}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_read_group_members_missing_param_who_has_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/group/members",
        json={},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 422


def test_read_group_members_missing_param_who_has_not_logged_in(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/group/members",
        json={},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
