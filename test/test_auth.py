import httpx
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

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


client = httpx.AsyncClient()


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


@pytest.fixture(scope="module")
def get_token_id():
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    refresh_token = "1//04puCTtWhEyMiCgYIARAAGAQSNwF-L9IrfZCxCMa5klAX2MxipBNzCbCr2rEgddoS7ejTrWJL9Oza8TJnBcoZPXg6EQgYK3Nwh4w"  # SDM
    # refresh_token = "1//048_5yRM12FFvCgYIARAAGAQSNwF-L9IrdAP1F8Kl_5tpnrTALjwUscnYjsUsl056-S0LCznkp3TZdMHUClAAZUN33XLenEQuL04"  # me
    # access_token = "ya29.a0Ael9sCMnHqRrjWZkL1l7bZuz3IXXTpKtJ90aiiw0pHbneWgIuFA-6MEFWjcEs7ZpKvMmKE67mkrp5Fu6wJYXmhK2cLACneHOIDgrbMB8j3Y6-cmmEVaoNWsOCxg21w3GnH0kUoIp6IOxeLFoUSWJm8xzPgPxaCgYKAfgSARMSFQF4udJhqsJNcq5l_FTXN0nRGIbnTA0163" #me
    post_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = httpx.post("https://oauth2.googleapis.com/token", json=post_body)

    id_token = response.json()["id_token"]

    return id_token


# test
def test_google_auth_verify_id_token_successfully(
    get_server_api, get_token_id, test_client
):
    credential = get_token_id
    data = {"credential": credential}
    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/auth/sso-login", json=data
    )
    # 因為這個google身分沒有名字之類的info
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Missing some user info from google authentication. Please use another way to create new account."
    )
    # idinfo = id_token.verify_oauth2_token(
    #     credential,
    #     requests.Request(),
    #     settings.GOOGLE_CLIENT_ID,
    #     clock_skew_in_seconds=5,
    # )
    # email = idinfo["email"]
    # user = crud.user.get_by_email(db=session, email=email)

    # if user:
    #     assert response.status_code == 200
    # else:
    #     # 因為這個google身分沒有名字之類的info
    #     assert response.status_code == 400
    #     assert (
    #         response.json()["detail"]
    #         == "Missing some user info from google authentication. Please use another way to create new account."
    #     )


def test_google_auth_verify_id_token_failed(get_server_api, test_client):
    credential = "fake_token_id"
    data = {"credential": credential}
    response = test_client.post(
        f"{get_server_api}{settings.API_V1_STR}/auth/sso-login", json=data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
