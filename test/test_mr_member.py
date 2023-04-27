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
import unittest

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


class Test_MR_Member:
    # data
    """  
    email = str
    name = str
    password = str
    created_user = dict
    created_room = dict
    """
    email = ''
    name = ''
    password = ''
    created_user = {}
    created_room = {}
    member_id = ''

    def __init__(self, email, name, password) -> None:
        self.email = email
        self.name = name
        self.password = password
     

# data for testing
test_mr_member = Test_MR_Member(
    email = random_lower_string() + "@example.com",
    name = random_lower_string(),
    password = random_lower_string())

def test_create_mr_member():
    # create user
    data = {"email": test_mr_member.email, "name": test_mr_member.name, "password": test_mr_member.password}
    response = client.post(f"{settings.API_V1_STR}/users/", json=data)
    test_mr_member.created_user = response.json()["data"]

    # matching room
    response = client.post(
        f"{settings.API_V1_STR}/matching-room/create",
        json={"name": "test_mr", "due_time": "2023-04-06T01:27:50.024Z",
            "min_member_num": 3, "description": "desc", "is_forced_matching": False},
        headers=get_user_authentication_headers(),

    )
    test_mr_member.created_room = response.json()["data"]

    # mr_member
    response = client.post(
        f"{settings.API_V1_STR}/mr-member/create",
        json={
                "user": {
                    "email": test_mr_member.email,
                    "is_admin": False,
                    "name": test_mr_member.name
                },
                "matching_room": {
                    "room_id": test_mr_member.created_room["room_id"]
                }
            },
        headers=get_user_authentication_headers(),
    )

    test_mr_member.member_id = response.json()["data"]["member_id"]

    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert response.json()["data"]["user"]["email"] == test_mr_member.created_user["email"]
    assert response.json()["data"]["matching_room"] == test_mr_member.created_room

""" #???不能delete
def test_delete_mr_member(self) -> None:

    response = client.delete(
        f"{settings.API_V1_STR}/mr-member",
        json={
                "user": {
                    "email": test_mr_member.email,
                    "is_admin": False,
                    "name": test_mr_member.name
                },
                "matching_room": {
                    "room_id": test_mr_member.created_room["room_id"]
                }
            },
        headers=get_user_authentication_headers(),
    )
    # loguru.logger.info(response)
    assert response.status_code == 200
    # assert response.json()["message"] == "success"


    """

def test_mr_member_self_tag():
    loguru.logger.info({
                "mr_member": {
                    "member_id": test_mr_member.member_id
                },
                "tag_text_list": [
                    random_lower_string()
                ],
                "matching_room": test_mr_member.created_room
            },)

    # mr_member
    response = client.post(
        f"{settings.API_V1_STR}/mr-member-tag/create-self-tag",
        json={
                "mr_member":{
                    "member_id": test_mr_member.member_id
                },
                "tag_text_list":[random_lower_string()],
                "matching_room": test_mr_member.created_room
            },
        headers=get_user_authentication_headers(),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"

def test_mr_member_find_tag():
    loguru.logger.info({
                "mr_member": {
                    "member_id": test_mr_member.member_id
                },
                "tag_text_list": [
                    random_lower_string()
                ],
                "matching_room": test_mr_member.created_room
            },)

    # mr_member
    response = client.post(
        f"{settings.API_V1_STR}/mr-member-tag/create-find-tag",
        json={
                "mr_member":{
                    "member_id": test_mr_member.member_id
                },
                "tag_text_list":[random_lower_string()],
                "matching_room": test_mr_member.created_room
            },
        headers=get_user_authentication_headers(),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"
