import pytest
from app.db.setup_test import (get_on_admin_token, get_simple_user_token,
                               setup_login)
from fastapi.testclient import TestClient
from main import app

from tests.test_route_brand import TEST_BRAND_NAME, create_brand

client = TestClient(app)


DUMMY_USERNAME = "dummy"
DUMMY_USER_PASSWORD = "dummy"


def create_user_profile(client: TestClient, suffix: str):
    return client.post(
        "/v1/users/signup",
        json={
            "email": f"{DUMMY_USERNAME}_{suffix}@{DUMMY_USERNAME}.com",
            "username": f"{DUMMY_USERNAME}_{suffix}",
            "password": DUMMY_USER_PASSWORD
        },
    )


def update_username(client: TestClient, suffix: str, username: str, new_username: str, jwt_token: str):
    return client.put(
        "/v1/users/username_update",
        headers={"Authorization": jwt_token},
        data={
            "username": f"{username}",
            "new_username": f"{new_username}",
        },
    )


def login_user(client: TestClient, user_email: str, user_password: str):
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
    return response


def update_description(client: TestClient, suffix: str, username: str, description: str, jwt_token: str):
    return client.put(
        "/v1/users/description_update",
        headers={"Authorization": jwt_token},
        data={"username": f"{username}", "description": f"{description}"},
    )


def delete_user_profile(client: TestClient, suffix: str, jwt_token: str):
    return client.delete(
        f"/v1/users/delete/{DUMMY_USERNAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )


def get_user_profile(client: TestClient, suffix: str, jwt_token: str):
    return client.post(
        f"/v1/users/{DUMMY_USERNAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )


def get_login_token(suffix: str):
    return setup_login(f"{DUMMY_USERNAME}_{suffix}@{DUMMY_USERNAME}.com", DUMMY_USER_PASSWORD)


def make_user_admin_of_a_brand(client: TestClient, suffix: str, jwt_token: str, suffix_brand: str = ""):
    if not suffix_brand:
        suffix_brand = suffix
    return client.post(
        f"/v1/users/{DUMMY_USERNAME}_{suffix}/make_business_admin/{TEST_BRAND_NAME}_{suffix_brand}",
        headers={"Authorization": jwt_token}
    )


def revoke_user_admin_of_a_brand(client: TestClient, suffix: str, jwt_token: str, suffix_brand: str = ""):
    if not suffix_brand:
        suffix_brand = suffix
    return client.delete(
        f"/v1/users/{DUMMY_USERNAME}_{suffix}/revoke_business_admin/{TEST_BRAND_NAME}_{suffix_brand}",
        headers={"Authorization": jwt_token}
    )


def test_create_user_profile():
    suffix = "create_user_profile"
    response = create_user_profile(client, suffix)
    assert response.status_code == 200
    assert response.json()["email"] == f"{DUMMY_USERNAME}_{suffix}@{DUMMY_USERNAME}.com"
    assert response.json()["username"] == f"{DUMMY_USERNAME}_{suffix}"
    # assert response.json()["is_active"] is False


def test_user_delete_his_profile():
    suffix = "del_user_his_profile"
    create_user_profile(client, suffix)
    jwt_token = get_login_token(suffix)
    response = delete_user_profile(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json() == "user_profile is deleted!"


def test_user_delete_someone_else():
    suffix = "del_user_someone_else_as_user"
    create_user_profile(client, suffix)
    jwt_token = get_simple_user_token()
    response = delete_user_profile(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == f"you do not have the right to delete {DUMMY_USERNAME}_{suffix}"


def test_on_admin_delete_someone_else():
    suffix = "del_user_someone_else_as_admin"
    create_user_profile(client, suffix)
    jwt_token = get_on_admin_token()
    response = delete_user_profile(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json() == "user_profile is deleted!"


def test_user_get_himself():
    suffix = "user_get_himself"
    create_user_profile(client, suffix)
    jwt_token = get_login_token(suffix)
    response = get_user_profile(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["username"] == f"{DUMMY_USERNAME}_{suffix}"
    assert response.json()["email"] == f"{DUMMY_USERNAME}_{suffix}@{DUMMY_USERNAME}.com"
    assert 'hashed_password' not in response.json()


def test_user_get_someone_else():
    suffix = "user_get_someone_else"
    create_user_profile(client, suffix)
    jwt_token = get_simple_user_token()
    response = get_user_profile(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == f'you do not have the right to get the username {DUMMY_USERNAME}_{suffix}'


def test_on_admin_get_someone_else():
    suffix = "user_get_himself_as_admin"
    create_user_profile(client, suffix)
    jwt_token = get_on_admin_token()
    response = get_user_profile(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["username"] == f"{DUMMY_USERNAME}_{suffix}"
    assert response.json()["email"] == f"{DUMMY_USERNAME}_{suffix}@{DUMMY_USERNAME}.com"
    assert 'hashed_password' not in response.json()


def test_make_user_business_admin_from_on_admin():
    suffix = "make_user_business_admin_from_on_admin"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    create_user_profile(client, suffix)
    response = make_user_admin_of_a_brand(client, suffix, jwt_token)
    assert (
        response.json() == {
            "username": f"{DUMMY_USERNAME}_{suffix}",
            "role_name": "business_admin",
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}"
        }
    )


def test_make_user_business_admin_from_brand_admin():
    base_suffix = "make_user_business_admin_from_brand_admin"
    suffix_old_brand_admin = base_suffix + "_old_brand_admin"
    suffix_new_brand_admin = base_suffix + "_new_brand_admin"

    on_admin_token = get_on_admin_token()

    create_user_profile(client, suffix_old_brand_admin)
    create_user_profile(client, suffix_new_brand_admin)
    jwt_token = get_login_token(suffix_old_brand_admin)

    create_brand(client, base_suffix, on_admin_token)

    response = make_user_admin_of_a_brand(client, suffix_new_brand_admin, jwt_token)
    assert (
        response.json()["detail"]
        == 'Only ON-Limited Admins can create new Business Admins'
    )


def test_make_user_business_admin_from_simple_user():
    suffix = "make_user_business_admin_from_simple_user"
    jwt_token = get_simple_user_token()
    create_brand(client, suffix, jwt_token)
    create_user_profile(client, suffix)
    response = make_user_admin_of_a_brand(client, suffix, jwt_token)
    assert (
        response.json()["detail"]
        == 'Only ON-Limited Admins can create new Business Admins'
    )


def test_revoke_user_business_admin_from_on_admin():
    suffix = "revoke_user_business_admin_from_on_admin"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, jwt_token)

    response = revoke_user_admin_of_a_brand(client, suffix, jwt_token)
    assert (
        response.json()["user_type"] == "simple_user" and
        response.json()["username"] == f"{DUMMY_USERNAME}_{suffix}"
    )


def test_revoke_user_business_admin_from_same_brand_admin():
    base_suffix = "revoke_user_bus_admin_from_same_brand_admin"
    suffix_revoked_brand_admin = base_suffix + "_revoked"
    suffix_other_brand_admin = base_suffix + "_other"

    on_admin_token = get_on_admin_token()

    create_user_profile(client, suffix_revoked_brand_admin)
    create_user_profile(client, suffix_other_brand_admin)

    jwt_token = get_login_token(suffix_other_brand_admin)

    response = create_brand(client, base_suffix, on_admin_token)

    make_user_admin_of_a_brand(client, suffix_revoked_brand_admin, on_admin_token, base_suffix)
    make_user_admin_of_a_brand(client, suffix_other_brand_admin, on_admin_token, base_suffix)

    response = revoke_user_admin_of_a_brand(client, suffix_revoked_brand_admin, jwt_token, base_suffix)

    assert (
        response.json()["user_type"] == "simple_user" and
        response.json()["username"] == f"{DUMMY_USERNAME}_{suffix_revoked_brand_admin}"
    )


def test_revoke_user_business_admin_from_brand_admin():
    base_suffix = "revoke_user_bus_admin_from_diff_brand_admin"
    base_suffix_other_brand = "revoke_user_bus_admin_from_diff_brand_admin_2"
    suffix_revoked_brand_admin = base_suffix + "_revoked"
    suffix_other_brand_admin = base_suffix + "_other"

    on_admin_token = get_on_admin_token()

    create_user_profile(client, suffix_revoked_brand_admin)
    create_user_profile(client, suffix_other_brand_admin)

    jwt_token = get_login_token(suffix_other_brand_admin)

    response = create_brand(client, base_suffix, on_admin_token)

    make_user_admin_of_a_brand(client, suffix_revoked_brand_admin, on_admin_token, base_suffix)
    make_user_admin_of_a_brand(client, suffix_other_brand_admin, on_admin_token, base_suffix_other_brand)

    response = revoke_user_admin_of_a_brand(client, suffix_revoked_brand_admin, jwt_token, base_suffix)

    assert response.json()["detail"] == 'Only ON-Limited Admins or the brand admins can revoke Business Admin rights'


def test_revoke_user_business_admin_from_simple_user():
    base_suffix = "revoke_user_bus_admin_from_simple_user"
    suffix_revoked_brand_admin = base_suffix + "_revoked"

    on_admin_token = get_on_admin_token()

    create_user_profile(client, suffix_revoked_brand_admin)

    jwt_token = get_simple_user_token()

    response = create_brand(client, base_suffix, on_admin_token)

    make_user_admin_of_a_brand(client, suffix_revoked_brand_admin, on_admin_token, base_suffix)

    response = revoke_user_admin_of_a_brand(client, suffix_revoked_brand_admin, jwt_token, base_suffix)

    assert response.json()["detail"] == 'Only ON-Limited Admins or the brand admins can revoke Business Admin rights'


def test_update_user_with_existing_username():
    suffix1 = "existing_username_1"
    suffix2 = "existing_username_2"
    username = f"{DUMMY_USERNAME}_{suffix1}"
    create_user_profile(client, suffix1)
    create_user_profile(client, suffix2)
    new_username = f"{DUMMY_USERNAME}_{suffix2}"
    jwt_token = setup_login(f"{DUMMY_USERNAME}_{suffix1}@{DUMMY_USERNAME}.com", "dummy")
    response = update_username(client, suffix1, username, new_username, jwt_token)

    assert response.status_code == 200
    assert response.json()["detail"] == "That username is already taken. Please try another one."


def test_update_user_description():
    suffix = "update_description"
    username = f"{DUMMY_USERNAME}_{suffix}"
    create_user_profile(client, suffix)
    description = "test new description"
    jwt_token = setup_login(f"{DUMMY_USERNAME}_{suffix}@{DUMMY_USERNAME}.com", "dummy")
    response = update_description(client, suffix, username, description, jwt_token)
    assert response.status_code == 200
    assert response.json() == "UserProfile updated with success !"


def test_update_user_profile_username():
    suffix = "update_username"
    username = "user_test"
    new_username = suffix + "_user_123"
    jwt_token = setup_login("test@gmail.com", "123")
    response = update_username(client, suffix, username, new_username, jwt_token)
    assert response.status_code == 200
    assert response.json() == "UserProfile updated with success !"


def test_send_email(fm):
    fm.config.SUPPRESS_SEND = 1
    with fm.record_messages() as outbox:
        suffix = "send_email"
        response = create_user_profile(client, suffix)
        assert response.status_code == 200
        # assert response.json()["is_active"] == False
        assert outbox[0]['From'] == "dummy_test@dummy.com"
        assert outbox[0]['To'] == "dummy_send_email@dummy.com"
        assert outbox[0]['Subject'] == "Your verification code is Valid for 15min"


@pytest.mark.skip(reason="not working")
def test_confirm_email():
    response = client.get("/v1/users/confirm_email/b9")
    assert response.status_code == 200, response.json()
    assert response.json()["message"] == "test api"
