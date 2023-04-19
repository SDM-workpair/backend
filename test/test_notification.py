from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app  # Flask instance of the API

client = TestClient(app)


def test_get_my_notifications():
    response = client.post(
        f"{settings.API_V1_STR}/notification/my-list",
        json={"email": "admin@sdm-teamatch.com"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"
    # assert response.json()['data'][0]['content'] == '配對活動1的配對結果已完成可於我的群組內查看配對結果'


def test_get_my_notifications_missing_param():
    response = client.post(
        f"{settings.API_V1_STR}/notification/my-list",
        json={},
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Fail to retrieve user's notifications. Missing parameter: email."
    )


def test_get_my_notifications_user_not_found():
    response = client.post(
        f"{settings.API_V1_STR}/notification/my-list",
        json={"email": "non-registered@gmail.com"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Fail to find user with this email."
