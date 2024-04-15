from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app

from tests.test_route_user_profile import (DUMMY_USERNAME, TEST_BRAND_NAME,
                                   create_brand, create_user_profile, get_login_token,
                                   make_user_admin_of_a_brand)

client = TestClient(app)


def get_all_roles_of_a_brand(client: TestClient, suffix: str, jwt_token: str):
    return client.get(
        f"/v1/roles/brand/{TEST_BRAND_NAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )


def get_roles_of_a_user(client: TestClient, suffix: str, jwt_token: str):
    return client.get(
        f"/v1/roles/user/{DUMMY_USERNAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )


def test_get_all_roles_of_a_brand_as_on_admin():
    base_suffix = "get_all_roles_of_a_brand_as_on_admin"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_admin_2 = base_suffix + "_2"

    jwt_token = get_on_admin_token()
    create_brand(client, base_suffix, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)
    create_user_profile(client, suffix_brand_admin_2)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, base_suffix)
    make_user_admin_of_a_brand(client, suffix_brand_admin_2, jwt_token, base_suffix)

    all_roles_of_a_brand = get_all_roles_of_a_brand(client, base_suffix, jwt_token)

    assert len(all_roles_of_a_brand.json()) == 2


def test_get_all_roles_of_a_brand_as_same_brand_admin():
    base_suffix = "get_all_roles_of_a_brand_as_same_brand_admin"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_admin_2 = base_suffix + "_2"

    jwt_token = get_on_admin_token()
    create_brand(client, base_suffix, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)
    create_user_profile(client, suffix_brand_admin_2)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, base_suffix)
    make_user_admin_of_a_brand(client, suffix_brand_admin_2, jwt_token, base_suffix)

    jwt_token = get_login_token(suffix_brand_admin_1)

    all_roles_of_a_brand = get_all_roles_of_a_brand(client, base_suffix, jwt_token)

    assert len(all_roles_of_a_brand.json()) == 2


def test_get_all_roles_of_a_brand_as_different_brand_admin():
    base_suffix = "get_all_roles_of_a_brand_as_diff_brand_admin"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_admin_2 = base_suffix + "_2"
    suffix_brand_admin_3 = base_suffix + "_3"
    suffix_brand_1 = base_suffix + "_b1"
    suffix_brand_2 = base_suffix + "_b2"

    jwt_token = get_on_admin_token()
    create_brand(client, suffix_brand_1, jwt_token)
    create_brand(client, suffix_brand_2, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)
    create_user_profile(client, suffix_brand_admin_2)
    create_user_profile(client, suffix_brand_admin_3)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_1)
    make_user_admin_of_a_brand(client, suffix_brand_admin_2, jwt_token, suffix_brand_1)
    make_user_admin_of_a_brand(client, suffix_brand_admin_3, jwt_token, suffix_brand_2)

    jwt_token = get_login_token(suffix_brand_admin_3)

    all_roles_of_a_brand = get_all_roles_of_a_brand(client, suffix_brand_1, jwt_token)

    assert all_roles_of_a_brand.json()["detail"] == f'you are not admin of the brand {TEST_BRAND_NAME}_{suffix_brand_1}'


def test_get_all_roles_of_a_brand_as_simple_user():
    base_suffix = "get_all_roles_of_a_brand_as_simple_user"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_admin_2 = base_suffix + "_2"

    jwt_token = get_on_admin_token()
    create_brand(client, base_suffix, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)
    create_user_profile(client, suffix_brand_admin_2)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, base_suffix)
    make_user_admin_of_a_brand(client, suffix_brand_admin_2, jwt_token, base_suffix)

    jwt_token = get_simple_user_token()

    all_roles_of_a_brand = get_all_roles_of_a_brand(client, base_suffix, jwt_token)

    assert all_roles_of_a_brand.json()["detail"] == "only brand admins and ON-Limited admins can access this route"


def test_get_roles_of_a_user_as_on_admin():
    base_suffix = "get_all_roles_of_a_user_as_on_admin"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_1 = base_suffix + "_b1"
    suffix_brand_2 = base_suffix + "_b2"

    jwt_token = get_on_admin_token()
    create_brand(client, suffix_brand_1, jwt_token)
    create_brand(client, suffix_brand_2, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_1)
    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_2)

    response = get_roles_of_a_user(client, suffix_brand_admin_1, jwt_token)
    assert len(response.json()) == 2


def test_get_roles_of_a_user_as_self():
    base_suffix = "get_all_roles_of_a_user_as_self"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_1 = base_suffix + "_b1"
    suffix_brand_2 = base_suffix + "_b2"

    jwt_token = get_on_admin_token()
    create_brand(client, suffix_brand_1, jwt_token)
    create_brand(client, suffix_brand_2, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_1)
    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_2)

    jwt_token = get_login_token(suffix_brand_admin_1)
    response = get_roles_of_a_user(client, suffix_brand_admin_1, jwt_token)
    assert len(response.json()) == 2


def test_get_roles_of_a_user_as_brand_admin():
    base_suffix = "get_all_roles_of_a_user_as_brand_admin"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_admin_2 = base_suffix + "_2"
    suffix_brand_admin_3 = base_suffix + "_3"
    suffix_brand_1 = base_suffix + "_b1"
    suffix_brand_2 = base_suffix + "_b2"
    suffix_brand_3 = base_suffix + "_b3"

    jwt_token = get_on_admin_token()
    create_brand(client, suffix_brand_1, jwt_token)
    create_brand(client, suffix_brand_2, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)
    create_user_profile(client, suffix_brand_admin_2)
    create_user_profile(client, suffix_brand_admin_3)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_1)
    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_2)
    make_user_admin_of_a_brand(client, suffix_brand_admin_2, jwt_token, suffix_brand_2)
    make_user_admin_of_a_brand(client, suffix_brand_admin_3, jwt_token, suffix_brand_3)

    jwt_token = get_login_token(suffix_brand_admin_1)
    response = get_roles_of_a_user(client, suffix_brand_admin_1, jwt_token)
    assert len(response.json()) == 2

    jwt_token = get_login_token(suffix_brand_admin_2)
    response = get_roles_of_a_user(client, suffix_brand_admin_1, jwt_token)
    assert len(response.json()) == 1

    jwt_token = get_login_token(suffix_brand_admin_3)
    response = get_roles_of_a_user(client, suffix_brand_admin_1, jwt_token)
    assert response.json()['detail'] == 'you cannot access the roles of someone else..'


def test_get_roles_of_a_user_as_simple_user():
    base_suffix = "get_all_roles_of_a_user_as_simple_user"
    suffix_brand_admin_1 = base_suffix + "_1"
    suffix_brand_1 = base_suffix + "_b1"
    suffix_brand_2 = base_suffix + "_b2"

    jwt_token = get_on_admin_token()
    create_brand(client, suffix_brand_1, jwt_token)
    create_brand(client, suffix_brand_2, jwt_token)

    create_user_profile(client, suffix_brand_admin_1)

    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_1)
    make_user_admin_of_a_brand(client, suffix_brand_admin_1, jwt_token, suffix_brand_2)

    jwt_token = get_simple_user_token()
    response = get_roles_of_a_user(client, suffix_brand_admin_1, jwt_token)
    assert response.json()['detail'] == 'you cannot access the roles of someone else..'
