from datetime import timedelta

import pytest
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.database.base_class import Base

# from app.database.session import db_session
from app.main import app  # Flask instance of the API
from app.routers.deps import get_db

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@\
{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/test.db"

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

# Set up the database once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# This fixture creates a nested transaction,
# recreates it when the application code calls session.commit
# and rolls it back at the end.
# Based on: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


# A fixture for the fastapi test client which depends on the
# previous session fixture. Instead of creating a new session in the
# dependency override, it uses the one provided by the session fixture.
@pytest.fixture()
def test_client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


# client = TestClient(app)


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


def get_user_authentication_headers(session):
    email = "test_admin@sdm-teamatch.com"

    user = crud.user.get_by_email(db=session, email=email)
    user = jsonable_encoder(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user["user_uuid"], expires_delta=access_token_expires
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


# Test
def test_read_user_me_who_has_logged_in(get_server_api, session, test_client):
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(
            email="test_admin@sdm-teamatch.com", name="test_admin", is_google_sso=True
        ),
    )
    email = "test_admin@sdm-teamatch.com"

    response = test_client.get(
        f"{get_server_api}{settings.API_V1_STR}/users/profile/me/",
        headers=get_user_authentication_headers(session),
    )

    assert response.status_code == 200
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"


def test_read_user_me_who_has_not_logged_in(get_server_api, test_client):
    response = test_client.get(
        f"{get_server_api}{settings.API_V1_STR}/users/profile/me/"
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_read_user_me_who_has_wrong_credential(get_server_api, test_client):
    response = test_client.get(
        f"{get_server_api}{settings.API_V1_STR}/users/profile/me/",
        headers={"Authorization": "Bearer wrongToken"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough segments"


def test_update_logged_in_user_profile(get_server_api, session, test_client):
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(
            email="test_admin@sdm-teamatch.com", name="test_admin", is_google_sso=True
        ),
    )
    email = "test_admin@sdm-teamatch.com"

    line_id = "fake_line_id"
    update_data = {"line_id": line_id}

    response = test_client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile",
        json=update_data,
        headers=get_user_authentication_headers(session),
    )
    assert response.status_code == 200
    assert email == response.json()["data"]["email"]
    assert response.json()["message"] == "success"


def test_update_user_profile_who_has_not_logged_in(get_server_api, test_client):
    update_data = {"line_id": "fake_line_id"}
    response = test_client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile", json=update_data
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_user_profile_who_has_wrong_credential(get_server_api, test_client):
    update_data = {"line_id": "fake_line_id"}
    response = test_client.put(
        f"{get_server_api}{settings.API_V1_STR}/users/profile",
        json=update_data,
        headers={"Authorization": "Bearer wrongToken"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough segments"


def test_create_new_user(get_server_api, test_client):
    email = "new_user@example.com"
    name = "new user"
    password = "newuser"
    data = {"email": email, "name": name, "password": password}
    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/users/", json=data
    )
    assert 200 <= response.status_code < 300
    created_user = response.json()
    assert email == created_user["data"]["email"]


def test_create_existing_user(get_server_api, session, test_client):
    crud.user.create(
        session,
        obj_in=schemas.UserCreate(
            email="test_admin@sdm-teamatch.com", name="test_admin", is_google_sso=True
        ),
    )
    email = "test_admin@sdm-teamatch.com"
    name = "test_admin"

    data = {"email": email, "name": name}
    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/users/", json=data
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "The user with this username already exists in the system."
    )
