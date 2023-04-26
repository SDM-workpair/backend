from fastapi.testclient import TestClient
import random
import string
from app.core.config import settings
from app.main import app  # Flask instance of the API
from app import crud
from app.database.session import db_session
import loguru
from app.schemas import UserCreate

from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from app.core import security


client = TestClient(app)

def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))

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


def test_create_mr_member():
    # user
    email = random_lower_string() + "@example.com"
    name = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": name, "password": password}
    response = client.post(f"{settings.API_V1_STR}/users/", json=data)
    created_user = response.json()["data"]

    # matching room
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/create",
        json={"name": "test_mr", "due_time": "2023-04-06T01:27:50.024Z",
              "min_member_num": 3, "description": "desc", "is_forced_matching": False},
        headers=get_user_authentication_headers(),

    )
    created_room = response.json()["data"]

    # mr_member
    response = client.post(
        f"{settings.API_V1_STR}/mr-member/create",
        json={
                "user": {
                    "email": email,
                    "is_admin": False,
                    "name": name
                },
                "matching_room": {
                    "room_id": created_room["room_id"]
                }
            },
        headers=get_user_authentication_headers(),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"]["user"]["email"] == created_user["email"]
    assert response.json()["data"]["matching_room"] == created_room



