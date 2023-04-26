import json
import unittest
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
fake_matching_room = schemas.MatchingRoom(
    room_id="test_room_id", due_time=datetime.now(), min_member_num=3
)
fake_matching_room.name = "test_matching_room"
fake_matching_room.description = "test_desc"
fake_matching_room.is_forced_matching = True
fake_matching_room.created_time = None


def create_session_cookie(data) -> str:
    signer = TimestampSigner(str(settings.GOOGLE_SECRET_KEY))

def test_create_matching_room():
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/create",
        json={"name": "test_mr", "due_time": "2023-04-06T01:27:50.024Z",
              "min_member_num": 3, "description": "desc", "is_forced_matching": False}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'success'
    assert response.json()['data']['name'] == 'test_mr'


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


class TestMatchingRoomAPI(unittest.TestCase):
    @mock.patch(
        "app.routers.api_v1.matching_room.crud.matching_room.search_with_user_and_name"
    )
    def test_read_my_matching_rooms_who_has_logged_in(self, mock_my_matching_rooms):
        mock_my_matching_rooms.return_value = [fake_matching_room]

        response = client.get(
            f"{settings.API_V1_STR}/matching-room/my-list",
            headers=get_user_authentication_headers(),
        )

        assert response.json()["data"][0]["room_id"] == fake_matching_room.room_id

    def test_read_my_matching_rooms_who_has_not_logged_in(self):
        response = client.get(f"{settings.API_V1_STR}/matching-room/my-list")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @mock.patch(
        "app.routers.api_v1.search.crud.matching_room.search_with_user_and_name"
    )
    def test_search_matching_rooms_who_has_logged_in(self, mock_matching_rooms):
        mock_matching_rooms.return_value = [fake_matching_room]

        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": True},
            headers=get_user_authentication_headers(),
        )

        assert response.json()["data"][0]["room_id"] == fake_matching_room.room_id

    def test_search_matching_rooms_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": True},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @mock.patch(
        "app.routers.api_v1.search.crud.matching_room.search_with_user_and_name"
    )
    def test_search_matching_rooms_with_user_who_has_logged_in(
        self, mock_matching_rooms
    ):
        mock_matching_rooms.return_value = [fake_matching_room]

        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": False},
            headers=get_user_authentication_headers(),
        )

        assert response.json()["data"][0]["room_id"] == fake_matching_room.room_id

    def test_search_matching_rooms_with_user_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM", "query_all": False},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_search_matching_rooms_missing_param_who_has_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": "SDM"},
            headers=get_user_authentication_headers(),
        )
        assert response.status_code == 422

    def test_search_matching_rooms_missing_param_who_has_not_logged_in(self):
        response = client.post(
            f"{settings.API_V1_STR}/search/matching-room/list",
            json={"prompt": ""},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
