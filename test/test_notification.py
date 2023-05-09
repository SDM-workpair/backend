from datetime import datetime

from app import crud, schemas
from app.core.config import settings

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
    assert (
        response.json()["data"][0]["receiver_uuid"]
        == "397d0336-3df4-4325-a1b3-cc4ef8e8e0ab"
    )


def test_read_my_notifications_who_has_not_logged_in(db_conn, test_client):
    response = test_client.get(f"{settings.API_V1_STR}/notification/my-list")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# test create notification function directly with CRUD (not through API)


def test_create_notification(db_conn):
    notification_obj = schemas.NotificationSendObjectModel(
        receiver_uuid="397d0336-3df4-4325-a1b3-cc4ef8e8e0ab",
        sender_uuid="2be6b063-8914-42b6-9e8d-1bbe14317cc2",
        template_uuid="9c1dc87f-e938-4fa1-9900-9b4ebd5701da",
        f_string="測試配對結果",
    )
    insert_obj = schemas.notification.NotificationCreate(
        receiver_uuid=notification_obj.receiver_uuid,
        sender_uuid=notification_obj.sender_uuid,
        send_time=datetime.now(),
        template_uuid=notification_obj.template_uuid,
        f_string=notification_obj.f_string,
    )
    crud.notification.create(db=db_conn, obj_in=insert_obj)
    query_result = crud.notification.get_by_receiver_uuid(
        db=db_conn, receiver_uuid="397d0336-3df4-4325-a1b3-cc4ef8e8e0ab"
    )[0]
    assert str(query_result.receiver_uuid) == "397d0336-3df4-4325-a1b3-cc4ef8e8e0ab"
