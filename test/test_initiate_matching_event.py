from app.core.config import settings

from .contest import db_conn, get_user_authentication_headers, test_client

"""
pytest fixture
"""
db_conn = db_conn
test_client = test_client
email = "admin@sdm-teamatch.com"

"""
Test Initiate Matching Event
"""


def test_initiate_matching_event(db_conn, test_client):
    response = test_client.post(
        f"{settings.API_V1_STR}/matching-event",
        json={"room_id": "IR001", "min_member_num": 2},
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
