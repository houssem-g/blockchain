import asyncio
import os
from typing import Union

from fastapi.testclient import TestClient
from pydantic import EmailStr

from app.api.utils.base.role import BRAND_ROLE_NAMES_DICT
from app.db.table_manager import TableManager
from main import app

client = TestClient(app)
TEST_SIMPLE_USER_EMAIL = "test@gmail.com"
TEST_SIMPLE_USER_NAME = "user_test"
TEST_SIMPLE_USER_PASSWORD = "123"
TEST_SIMPLE_USER_DESCRIPTION = "NFT Collector"

TEST_ON_ADMIN_USER_NAME = os.environ.get("USER_NAME", "test")
TEST_ON_ADMIN_PASSWORD = os.environ.get("PASSWORD", "testdb")
TEST_ON_ADMIN_EMAIL = f"{TEST_ON_ADMIN_USER_NAME}@on-limited.com"
TEST_ON_ADMIN_DESCRIPTION = "Admin manager"

 
def get_simple_user_token():
    env_token = os.environ.get("TEST_SIMPLE_USER_TOKEN")
    if env_token is not None:
        return env_token
    else:
        return ""


def get_on_admin_token():
    env_token = os.environ.get("TEST_ON_ADMIN_TOKEN")
    if env_token is not None:
        return env_token
    else:
        return ""


def setup_login(user_email: str, user_password: str, env_variable: Union[str, None] = None):
    print(f"we setup the test login for {env_variable}")
    data = {
        "grant_type": "",
        "username": user_email,
        "password": user_password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    response = client.post(
        "/v1/users/login",
        headers={"X-Token": "coneofsilence"},
        data=data,
    )

    assert "access_token" in response.json(), response.json()
    jwt = "Bearer " + response.json()["access_token"]
    if env_variable:
        os.environ[env_variable] = str(jwt)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    return str(jwt)


def setup_roles():
    for role_name in BRAND_ROLE_NAMES_DICT:
        response = client.post(
            "/v1/roles",
            headers={"Authorization": get_on_admin_token()},
            json={"role_name": role_name},
        )
        assert response.json() == {"role_name": role_name}
    print(f"roles {BRAND_ROLE_NAMES_DICT} are setup")


async def setup_test():

    table_manager = TableManager()
    await table_manager.create_simple_user(
        EmailStr(TEST_SIMPLE_USER_EMAIL), TEST_SIMPLE_USER_NAME, TEST_SIMPLE_USER_PASSWORD
    )
    setup_login(TEST_SIMPLE_USER_EMAIL, TEST_SIMPLE_USER_PASSWORD, "TEST_SIMPLE_USER_TOKEN")
    setup_login(TEST_ON_ADMIN_EMAIL, TEST_ON_ADMIN_PASSWORD, "TEST_ON_ADMIN_TOKEN")
    setup_roles()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_test())


if __name__ == "__main__":
    main()
