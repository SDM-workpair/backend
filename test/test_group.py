import json
import unittest
import uuid
from base64 import b64encode
from datetime import datetime, timedelta
from unittest import mock

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from itsdangerous import TimestampSigner

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.database.session import db_session
from app.main import app  # Flask instance of the API

client = TestClient(app)

# fake data for test
fake_group = schemas.Group(
    name="test_group_name",
    group_id="test_group_id",
    room_uuid=uuid.uuid4(),
    create_time=datetime.now(),
)
fake_member = schemas.User(
    email="test-email@gmail.com",
    is_admin=True,
    name="test_name",
    line_id="test_line_id",
    image="",
)


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


class TestGroupAPI(unittest.TestCase):
    @mock.patch("app.routers.api_v1.group.crud.group.search_with_user_and_name")
    def test_read_my_groups_who_has_logged_in(self, mock_my_groups):
        mock_my_groups.return_value = [fake_group]

        response = client.get(
            f"{settings.API_V1_STR}/group/my-list",
            headers=get_user_authentication_headers(),
        )

        assert response.json()["data"][0]["group_id"] == fake_group.group_id

    def test_read_my_groups_who_has_not_logged_in(self):
        response = client.get(f"{settings.API_V1_STR}/group/my-list")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @mock.patch("app.routers.api_v1.search.crud.group.search_with_user_and_name")
    def test_search_groups_who_has_logged_in(self, mock_groups):
        mock_groups.return_value = [fake_group]

        response = client.post(
            f"{settings.API_V1_STR}/search/group/list",
            json={"prompt": "test"},
            headers=get_user_authentication_headers(),
        )

        assert response.json()["data"][0]["group_id"] == fake_group.group_id

    def test_search_groups_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/group/list", json={"prompt": "test"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @mock.patch("app.routers.api_v1.search.crud.group.search_with_user_and_name")
    def test_search_groups_missing_param_who_has_logged_in(self, mock_groups):
        mock_groups.return_value = [fake_group]

        response = client.post(
            f"{settings.API_V1_STR}/search/group/list",
            json={},
            headers=get_user_authentication_headers(),
        )
        assert response.status_code == 422

    def test_search_groups_missing_param_who_has_not_logged_in(self):
        response = client.post(f"{settings.API_V1_STR}/search/group/list", json={})
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @mock.patch("app.routers.api_v1.group.crud.gr_member.get_all_members_by_group_id")
    def test_read_group_members_who_has_logged_in(self, mock_group_members):
        mock_group_members.return_value = [fake_member]

        response = client.post(
            f"{settings.API_V1_STR}/group/members",
            json={"group_id": "test"},
            headers=get_user_authentication_headers(),
        )

        assert response.json()["data"][0]["email"] == fake_member.email

    def test_read_group_members_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/group/members", json={"group_id": ""}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_read_group_members_empty_group_id_who_has__logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/group/members",
            json={"group_id": ""},
            headers=get_user_authentication_headers(),
        )

        assert response.status_code == 400
        assert (
            response.json()["detail"]
            == "Fail to get group members. Missing parameter: group_id."
        )

    def test_read_group_members_empty_group_id_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/group/members", json={"group_id": ""}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_read_group_members_missing_param_who_has_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/group/members",
            json={},
            headers=get_user_authentication_headers(),
        )
        assert response.status_code == 422

    def test_read_group_members_missing_param_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/group/members",
            json={},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
