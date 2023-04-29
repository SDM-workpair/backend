import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from app.core.config import settings
from app.database.base_class import Base
from app.main import app
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


# TEMPLATE
# 如果 API 用到 db 的 session(Depends(deps.get_db))，
# 在 function 參數放 test_client ，用上面 pytest.fixture 的 test_client
# def test_something(test_client):
#     response = test_client.get("/test-something")
#     assert response.status_code == 200

# 如果會用到 crud ，
# 在 function 參數放 session ，用上面 pytest.fixture 的 session
# def test_something(session):
#     crud.something.get_by_id(session, ...)

# 如果 API 用到 db 的 session(Depends(deps.get_db))，也會用到 crud
# 在 function 參數兩個都放~用上面 pytest.fixture 的 test_client 和 session
# def test_something(session, test_client):
#     response = test_client.get("/test-something")
#     session.add()
#     session.commit()
#     assert response.status_code == 200
