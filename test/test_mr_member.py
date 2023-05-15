import random
import string

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
Test data
"""


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


class Test_MR_Member:
    email = ""
    name = ""
    password = ""
    created_user = {}
    created_room = {"room_id": 0}
    member_id = 0

    def __init__(self, email, name, password) -> None:
        self.email = email
        self.name = name
        self.password = password


test_mr_member = Test_MR_Member(
    email=random_lower_string() + "@example.com",
    name=random_lower_string(),
    password=random_lower_string(),
)


"""
Test case
"""


def test_create_mr_member(db_conn, test_client):
    # create user
    data = {
        "email": test_mr_member.email,
        "name": test_mr_member.name,
        "password": test_mr_member.password,
    }
    response = test_client.post(f"{settings.API_V1_STR}/users/", json=data)
    test_mr_member.created_user = response.json()["data"]

    # matching room
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
    test_mr_member.created_room["room_id"] = response.json()["data"]["room_id"]

    # mr_member
    response = test_client.post(
        f"{settings.API_V1_STR}/mr-member/create",
        json={
            "user": {
                "email": test_mr_member.email,
                "is_admin": False,
                "name": test_mr_member.name,
            },
            "matching_room": {"room_id": test_mr_member.created_room["room_id"]},
        },
        headers=get_user_authentication_headers(db_conn, email),
    )

    test_mr_member.member_id = response.json()["data"]["member_id"]

    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert (
        response.json()["data"]["user"]["email"] == test_mr_member.created_user["email"]
    )
    assert response.json()["data"]["matching_room"] == test_mr_member.created_room


def test_mr_member_self_tag(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/mr-member-tag/create-self-tag",
        json={
            "mr_member": {"member_id": test_mr_member.member_id},
            "tag_text_list": [random_lower_string()],
            "matching_room": test_mr_member.created_room,
        },
        headers=get_user_authentication_headers(db_conn, email),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"


def test_mr_member_find_tag(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/mr-member-tag/create-find-tag",
        json={
            "mr_member": {"member_id": test_mr_member.member_id},
            "tag_text_list": [random_lower_string()],
            "matching_room": test_mr_member.created_room,
        },
        headers=get_user_authentication_headers(db_conn, email),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"


"""
Delete API test
"""


def test_delete_mr_member(db_conn, test_client):
    response = test_client.request(
        "DELETE",
        f"{settings.API_V1_STR}/mr-member",
        json={
            "user": {
                "email": test_mr_member.email,
                "is_admin": False,
                "name": test_mr_member.name,
            },
            "matching_room": {"room_id": test_mr_member.created_room["room_id"]},
        },
        headers=get_user_authentication_headers(db_conn, email),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # delete test data
    delete_test_data(db_conn)


"""
Delete testing data
"""


def delete_test_data(db_conn):
    """
    # find tag
    obj = crud.mr_member_tag.get_1st_find_tag_by_member_id(
        db=db_conn, member_id=test_mr_member.member_id
    )
    db_conn.delete(obj)

    # self tag
    obj = crud.mr_member_tag.get_1st_self_tag_by_member_id(
        db=db_conn, member_id=test_mr_member.member_id
    )
    db_conn.delete(obj)
    db_conn.commit()

    # mr_member
    obj = crud.mr_member.get_by_member_id(
        db=db_conn, member_id=test_mr_member.member_id
    )
    db_conn.delete(obj)
    db_conn.commit()
    """
    # matching room
    obj = crud.matching_room.get_by_room_id(
        db_conn, room_id=test_mr_member.created_room["room_id"]
    )
    db_conn.delete(obj)
    db_conn.commit()

    # user
    obj = crud.user.get_by_email(db_conn, email=test_mr_member.email)
    db_conn.delete(obj)
    db_conn.commit()

    return
