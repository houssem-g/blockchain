from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app
from tests.item.utils import create_item, delete_item
from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_category import create_category
from tests.test_route_item_class import TEST_PN, create_item_class
from tests.test_route_item_config import create_item_config
from tests.test_route_user_profile import (create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)


def test_delete_item_as_on_admin():
    suffix = "delete_item_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    response = delete_item(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["burn_status"] is False
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_delete_item_as_item_brand_admin():
    suffix = "del_item_config_as_item_conf_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    response = delete_item(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["burn_status"] is False
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_delete_item_as_other_brand_admin():
    base_suffix = "del_item"
    item_brand_suffix = base_suffix + "_item_brand"
    other_brand_suffix = base_suffix + "_other_brand"
    test_description_json = '{"color": "red_' + item_brand_suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, item_brand_suffix, on_admin_jwt)
    create_brand(client, other_brand_suffix, on_admin_jwt)
    create_category(client, item_brand_suffix, on_admin_jwt)
    create_item_class(client, item_brand_suffix, on_admin_jwt)
    create_item_config(client, item_brand_suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, item_brand_suffix, test_description_json, on_admin_jwt)
    create_user_profile(client, base_suffix)
    make_user_admin_of_a_brand(client, base_suffix, on_admin_jwt, other_brand_suffix)

    brand_admin_jwt = get_login_token(base_suffix)

    response = delete_item(client, item_brand_suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert "you are not admin of the brand " in response.json()['detail']


def test_delete_item_as_simple_user():
    suffix = "delete_item_as_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    response = delete_item(client, suffix, get_simple_user_token())

    assert response.status_code == 200
    assert response.json()['detail'] == 'you do not have the right to delete items..'
