from fastapi.testclient import TestClient
import random
import string
from app.core.config import settings
from app.main import app  # Flask instance of the API

client = TestClient(app)

def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


# def test_create_mr_member():
#     email = random_lower_string() + "@example.com"
#     name = random_lower_string()
#     password = random_lower_string()
#     data = {"email": email, "name": name, "password": password}
#     response = client.post(f"{settings.API_V1_STR}/users/", json=data)
#     assert 200 <= response.status_code < 300
#     created_user = response.json()
#     assert email == created_user["data"]["email"]



#     response = client.post(
#         f"{settings.API_V1_STR}/mr_member/create",
#         json={
#                 "user": {
#                     "email": email,
#                     "is_admin": false,
#                     "name": name
#                 },
#                 "matching_room": {
#                     "room_id": "eb606a"
#                 }
#             }
#     )
#     assert response.status_code == 200
#     assert response.json()['message'] == 'success'
#     assert response.json()['data']['name'] == 'test_mr'



