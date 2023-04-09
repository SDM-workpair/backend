import json
import random
import string
from base64 import b64encode

import pytest
from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from app.core.config import settings
from app.main import app  # Flask instance of the API

# client = TestClient(app)


# @pytest.fixture(scope="module")           #new function
# def normal_user_token_headers(client: TestClient, db_session: Session):
#     return  authentication_token_from_email(
#         client=client, email=settings.TEST_USER_EMAIL, db=db_session
#     )
@pytest.fixture(scope="module")
def get_test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
def get_server_api():
    server_name = f"http://localhost:8000"
    return server_name


# @pytest.fixture(scope="module")
# def get_user_token_headers():
#     server_api = get_server_api()
#     login_data = {
#         "username": "user1",
#         "password": "string",
#     }
#     response = client.post(
#         f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
#     )
#     tokens = response.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     # user_token_headers = headers
#     return headers


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_session_cookie(data) -> str:
    signer = TimestampSigner(str(settings.GOOGLE_SECRET_KEY))

    return signer.sign(
        b64encode(json.dumps(data).encode("utf-8")),
    ).decode("utf-8")


# Test
def test_read_user_me_who_has_logged_in(get_test_client, get_server_api):
    client = get_test_client
    # create new google sso user
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password, "is_google_sso": True}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)
    user = response.json()["data"]

    response = client.get(
        f"{get_server_api}{settings.API_V1_STR}/users/profile/me/",
        cookies={"session": create_session_cookie({"user": user})},
    )
    client.get(f"{get_server_api}{settings.API_V1_STR}/users/logout")
    assert 200 <= response.status_code < 300
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"


def test_read_user_me_who_has_not_logged_in(get_test_client, get_server_api):
    client = get_test_client
    # create new google sso user
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password, "is_google_sso": True}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)

    response = client.get(f"{get_server_api}{settings.API_V1_STR}/users/profile/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials."


def test_update_logged_in_user_profile(get_test_client, get_server_api):
    client = get_test_client
    # create new google sso user
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password, "is_google_sso": True}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)
    line_id = random_lower_string()
    update_data = {"line_id": line_id}
    response = client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile",
        json=update_data,
        cookies={"session": create_session_cookie({"user": response.json()["data"]})},
    )
    client.get(f"{get_server_api}{settings.API_V1_STR}/users/logout")
    assert 200 <= response.status_code < 300
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"


def test_update_user_profile_who_has_not_logged_in(get_test_client, get_server_api):
    client = get_test_client
    # create new google sso user
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password, "is_google_sso": True}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)
    update_data = {"line_id": "98765"}
    response = client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile", json=update_data
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials."


def test_create_new_user(get_test_client, get_server_api):
    client = get_test_client
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password}
    response = client.post(
        f"{get_server_api}{settings.API_V1_STR}/users/", json=data, cookies={}
    )
    assert 200 <= response.status_code < 300
    created_user = response.json()
    assert email == created_user["data"]["email"]


def test_create_existing_user(get_test_client, get_server_api):
    client = get_test_client
    email = "user1@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password}
    response = client.post(f"{get_server_api}{settings.API_V1_STR}/users/", json=data)
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "The user with this username already exists in the system."
    )


# def test_user_google_login():
