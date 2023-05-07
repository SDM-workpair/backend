import random
import string

import pytest

from app.core.config import settings
from app.models.mr_liked_hated_member import MR_Liked_Hated_Member

from .contest import db_conn, get_user_authentication_headers, test_client

# pytest fixture
db_conn = db_conn
test_client = test_client

# Fake data
# user
# fake_user = []
# for i in range(4):
#     obj_in = schemas.UserCreate(
#         email="test_admin" + str(i + 1) + "@sdm-teamatch.com",
#         name="test_admin" + str(i + 1),
#         is_google_sso=True,
#     )
#     fake_user.append(obj_in)
#     crud.user.create(
#         test_session,
#         obj_in=obj_in,
#     )
# # matching room
# matching_room_in = schemas.MatchingRoomCreate(
#     name="swipe_test_matching_room",
#     room_id="swipe_test_matching_room001",
#     due_time=datetime.datetime.now(),
#     min_member_num=3,
# )
# crud.matching_room.create(test_session, obj_in=matching_room_in)
# # MR_member
# user_uuids = []
# for i in range(4):
#     user = crud.user.get_by_email(
#         test_session, email="test_admin" + str(i + 1) + "@sdm-teamatch.com"
#     )
#     user_uuids.append(user.user_uuid)
# matching_room = crud.matching_room.get_by_room_id(
#     test_session, room_id="swipe_test_matching_room001"
# )
# room_uuid = jsonable_encoder(matching_room)["room_uuid"]
# for uuid in user_uuids:
#     mr_member_in1 = MR_Member(
#         user_uuid=uuid,
#         room_uuid=room_uuid,
#     )
#     test_session.add(mr_member_in1)
#     test_session.commit()


# def delete_fake_data():
#     # delete MR_Liked_Hated_Member
#     obj = (
#         test_session.query(MR_Liked_Hated_Member)
#         .filter(MR_Liked_Hated_Member.room_uuid == room_uuid)
#         .first()
#     )
#     test_session.delete(obj)
#     test_session.commit()
#     # delete mr member
#     for user_uuid in user_uuids:
#         obj = (
#             test_session.query(MR_Member)
#             .filter(MR_Member.user_uuid == user_uuid)
#             .first()
#         )
#         test_session.delete(obj)
#         test_session.commit()
#     # delete matching room
#     obj = (
#         test_session.query(MatchingRoom)
#         .filter(MatchingRoom.room_id == "swipe_test_matching_room001")
#         .first()
#     )
#     test_session.delete(obj)
#     test_session.commit()
#     # delete user
#     for user_uuid in user_uuids:
#         obj = test_session.query(User).filter(User.user_uuid == user_uuid).first()
#         test_session.delete(obj)
#         test_session.commit()


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


# def get_user_authentication_headers(session, email):
#     email = email

#     user = crud.user.get_by_email(db=session, email=email)
#     user = jsonable_encoder(user)
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = security.create_access_token(
#         user["user_uuid"], expires_delta=access_token_expires
#     )
#     headers = {"Authorization": f"Bearer {access_token}"}
#     return headers


# Test
def test_save_preference_who_has_logged_in(get_server_api, db_conn, test_client):
    # member = []
    # for i in range(2):
    #     member.append(
    #         jsonable_encoder(
    #             db_conn.query(MR_Member)
    #             .filter(MR_Member.user_uuid == user_uuids[i])
    #             .first()
    #         )
    #     )

    # preference = {
    #     "member_id": member[0]["member_id"],
    #     "room_uuid": room_uuid,
    #     "target_member_id": member[1]["member_id"],
    #     "is_like": True,
    #     "is_hated": False,
    # }
    preference = {
        "member_id": 2,
        "room_uuid": "15b14b78-7b33-4274-868f-e3aca152bd80",
        "target_member_id": 11,
        "is_like": True,
        "is_hated": False,
    }

    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe",
        headers=get_user_authentication_headers(
            session=db_conn, email="admin@sdm-teamatch.com"
        ),
        json=preference,
    )

    # delete mr_liked_hated_member
    mr_liked_hated_member = (
        db_conn.query(MR_Liked_Hated_Member)
        .filter(
            MR_Liked_Hated_Member.member_id == 2,
            MR_Liked_Hated_Member.target_member_id == 11,
        )
        .first()
    )
    db_conn.delete(mr_liked_hated_member)
    db_conn.commit()

    assert response.status_code == 200
    assert response.json()["message"] == "success"


def test_save_preference_who_has_not_logged_in(get_server_api, test_client):
    preference = {
        "member_id": "1",
        "room_uuid": "6891704b-a2e8-4fce-b971-b3fe3928dfd6",
        "target_member_id": "2",
        "is_like": True,
        "is_hated": False,
    }

    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe", json=preference
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_recommendation(get_server_api, db_conn, test_client):
    # member = jsonable_encoder(db_conn.query(MR_Member).first())

    # recommend_in = {"member_id": member["member_id"], "room_uuid": room_uuid}
    recommend_in = {"member_id": 3, "room_uuid": "58102867-1773-4c68-a78f-d6da7124bb2d"}

    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/swipe-card/swipe-recommend",
        headers=get_user_authentication_headers(
            session=db_conn, email="admin@sdm-teamatch.com"
        ),
        json=recommend_in,
    )
    response_data = response.json()["data"]
    rcmd_member_list = []
    for d in response_data:
        rcmd_member_list.append(d["recommended_member_id"])

    # delete fake data
    # delete_fake_data()

    assert response.status_code == 200
    assert response.json()["message"] == "success"
    assert len(rcmd_member_list) == 2
