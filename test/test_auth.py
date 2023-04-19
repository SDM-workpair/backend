import pytest
from fastapi.testclient import TestClient

from app.main import app  # Flask instance of the API

client = TestClient(app)


@pytest.fixture(scope="module")
def get_server_api():
    server_name = "http://localhost:8000"
    return server_name


# test
# def test_google_auth(get_server_api):
#     credential = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImFjZGEzNjBmYjM2Y2QxNWZmODNhZjgzZTE3M2Y0N2ZmYzM2ZDExMWMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2ODExNDM4MjYsImF1ZCI6Ijc2ODMwNTUzMzI1Ni1lZzNpZnQ5NnNwb2xndG02OWJvNnIzNDIzZGYxM2M3My5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwNTA2NzU1OTQ2Mjc4NTI3NTc5OCIsImVtYWlsIjoic2RtMjAyMy5ubzJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6Ijc2ODMwNTUzMzI1Ni1lZzNpZnQ5NnNwb2xndG02OWJvNnIzNDIzZGYxM2M3My5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJTRCBNIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FHTm15eFlOc0hQQVBjOHAzMkFzMzF3QXlmdU12elN2NXhrTEM0ZGNfLWFPPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IlNEIiwiZmFtaWx5X25hbWUiOiJNIiwiaWF0IjoxNjgxMTQ0MTI2LCJleHAiOjE2ODExNDc3MjYsImp0aSI6IjYyNThlZmNhYzFhNjcxNDIxNjJkMWYwMmU0MmI0ZGQ2OGFlODBjMmEifQ.bdDiJjnfuU-d2TLxnVfCocDSPVIhCtHA4A1pTBL3kjNBVGFi66DJZxS3w-gC_UKEytZnWaPjuWcjYaGKF4fjz1qlnPLuZiIPGq6z5tvf72RZ7s-tqPIemGHXoFxZdHaKc3JY3ys14jDdeSPUD7JYdGiVklKwdsNc1j8IvShHEnBIm8dnPQ-ozRKyT7gWPrEmF0zmA6rkYuiXsdHeHQ9-73cTmA-E-bhqKaVYDP7Jbhe7k0KPCpkIzQOyE4j-uuytSutU31yXB0d2I-6IpCDw0P8BDmqvwfIwXdYkU_7xbK_BRV4k6DnfnOysSOEuNqPrYqF4QNSyEYBzI7C-kDnPMw"
#     data = {"credential": credential}
#     response = client.post(
#         f"{get_server_api}{settings.API_V1_STR}/auth/sso-login", json=data
#     )
#     client.get(f"{get_server_api}{settings.API_V1_STR}/users/logout")
#     assert response.status_code == 200
