from fastapi.testclient import TestClient
import random
import string
from app.core.config import settings
from app.main import app  # Flask instance of the API
import loguru

client = TestClient(app)

def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


# def test_create_mr_member():
#     # user
#     email = random_lower_string() + "@example.com"
#     name = random_lower_string()
#     password = random_lower_string()
#     data = {"email": email, "name": name, "password": password}
#     response = client.post(f"{settings.API_V1_STR}/users/", json=data)
#     assert 200 <= response.status_code < 300
#     created_user = response.json()["data"]
#     assert email == created_user["email"]
#     # loguru.logger.info(created_user)
#     print(created_user)

#     # matching room
#     response = client.post(
#         f"{settings.API_V1_STR}/matching-room/create",
#         json={"name": "test_mr", "due_time": "2023-04-06T01:27:50.024Z",
#               "min_member_num": 3, "description": "desc", "is_forced_matching": False}
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "success"
#     created_room = response.json()["data"]
#     assert created_room["name"] == "test_mr"
#     # loguru.logger.info(created_room)
#     print(created_room)

#     # mr_member
#     response = client.post(
#         f"{settings.API_V1_STR}/mr_member/create",
#         json={
#                 "user": {
#                     "email": email,
#                     "is_admin": False,
#                     "name": name
#                 },
#                 "matching_room": {
#                     "room_id": created_room["room_id"]
#                 }
#             }
#     )
    # print(response.json()["message"])
#     assert response.status_code == 200
    # assert response.json()["message"] == "success"
    # assert response.json()["data"]["user"] == created_user
    # assert response.json()["data"]["matching_room"] == created_room



