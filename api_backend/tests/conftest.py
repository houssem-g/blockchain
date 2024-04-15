from fastapi.testclient import TestClient
from main import app
from fastapi_mail import FastMail, ConnectionConfig
import pytest
from app.db.setup_test import (
    TEST_ON_ADMIN_EMAIL,
    TEST_ON_ADMIN_PASSWORD,
    TEST_SIMPLE_USER_EMAIL,
    TEST_SIMPLE_USER_PASSWORD,
    setup_login,
)

client = TestClient(app)

# os.environ["WORKING_ENV"] = "test"

# Grab a reference to our database when needed
# @pytest.fixture
# def db(app: FastAPI) -> Database:
#     return app.state._db


# # Make requests in our tests
# # TODO: undestand
# @pytest.fixture
# async def client(app: FastAPI):
#     async with LifespanManager(app):
#         async with AsyncClient(
#             app=app, base_url="http://127.0.0.1", headers={"Content-Type": "application/json"}
#         ) as client:
#             yield client

def pytest_configure(config):
    setup_login(TEST_SIMPLE_USER_EMAIL, TEST_SIMPLE_USER_PASSWORD, "TEST_SIMPLE_USER_TOKEN")
    setup_login(TEST_ON_ADMIN_EMAIL, TEST_ON_ADMIN_PASSWORD, "TEST_ON_ADMIN_TOKEN")

conf = ConnectionConfig(
    MAIL_USERNAME = "YourUsername",
    MAIL_PASSWORD = "strong_password",
    MAIL_FROM = "your@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "your mail server",
    MAIL_TLS = True,
    MAIL_SSL = False,
    SUPPRESS_SEND=1

)

@pytest.fixture
def fm():
    
    mail = FastMail(conf)
    mail.config.SUPPRESS_SEND = 1
    return mail