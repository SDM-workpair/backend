import json
import random
import string
from base64 import b64encode
from datetime import timedelta

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from app import crud
from app.core import security
from app.core.config import settings
from app.database.session import db_session
from app.main import app  # Flask instance of the API

client = TestClient(app)


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_session_cookie(data) -> str:
    signer = TimestampSigner(str(settings.GOOGLE_SECRET_KEY))

    return signer.sign(
        b64encode(json.dumps(data).encode("utf-8")),
    ).decode("utf-8")


def get_user_authentication_headers():
    email = "admin@sdm-teamatch.com"

    user = crud.user.get_by_email(db=db_session, email=email)
    user = jsonable_encoder(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user["user_uuid"], expires_delta=access_token_expires
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


# Test
def test_read_user_me_who_has_logged_in(get_server_api):
    email = "admin@sdm-teamatch.com"

    response = client.get(
        f"{get_server_api}{settings.API_V1_STR}/users/profile/me/",
        headers=get_user_authentication_headers(),
    )

    assert response.status_code == 200
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"


def test_read_user_me_who_has_not_logged_in(get_server_api):
    response = client.get(f"{get_server_api}{settings.API_V1_STR}/users/profile/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_logged_in_user_profile(get_server_api):
    email = "admin@sdm-teamatch.com"

    line_id = random_lower_string()
    update_data = {"line_id": line_id}

    response = client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile",
        json=update_data,
        headers=get_user_authentication_headers(),
    )
    assert response.status_code == 200
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"


def test_update_user_profile_who_has_not_logged_in(get_server_api):
    update_data = {"line_id": "98765"}
    response = client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile", json=update_data
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_new_user(get_server_api):
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)
    assert 200 <= response.status_code < 300
    created_user = response.json()
    assert email == created_user["data"]["email"]


def test_create_existing_user(get_server_api):
    email = "admin@sdm-teamatch.com"
    name = "admin"
    password = "1234"
    data = {"email": email, "name": name, "password": password}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "The user with this username already exists in the system."
    )
