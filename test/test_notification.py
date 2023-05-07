from base64 import b64encode
from datetime import datetime
from app import crud, schemas, models
from app.core import security
from app.core.config import settings
from app.main import app  # Flask instance of the API
from .contest import db_conn, get_user_authentication_headers, test_client

"""
pytest fixture
"""
db_conn = db_conn
test_client = test_client
email = "admin@sdm-teamatch.com"

"""
Test Notification
"""


def test_read_my_notifications_who_has_logged_in(db_conn, test_client):
    response = test_client.get(
        f"{settings.API_V1_STR}/notification/my-list",
        headers=get_user_authentication_headers(db_conn, email),
    )
    assert response.status_code == 200
    assert response.json()[
        "data"][0]["receiver_uuid"] == "397d0336-3df4-4325-a1b3-cc4ef8e8e0ab"


def test_read_my_notifications_who_has_not_logged_in(db_conn, test_client):
    response = test_client.get(f"{settings.API_V1_STR}/notification/my-list")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
