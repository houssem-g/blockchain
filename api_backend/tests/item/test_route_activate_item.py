
from app.db.setup_test import get_on_admin_token
from fastapi.testclient import TestClient
from main import app
from tests.item.utils import (activate_item, create_item,
                              get_items_from_username)
from tests.test_route_brand import create_brand
from tests.test_route_category import create_category
from tests.test_route_item_class import TEST_PN, create_item_class
from tests.test_route_item_config import create_item_config
from tests.test_route_user_profile import create_user_profile, get_login_token

client = TestClient(app)


def test_activate_item_as_simple_user():
    suffix = "activate_item_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)

    user_jwt_token = get_login_token(suffix)

    activate_item(client, activation_key, user_jwt_token)

    final_user_items = get_items_from_username(client, suffix, user_jwt_token)

    assert (
        item_response.json()["serial_number"] in [item["serial_number"] for item in final_user_items.json()]
        ), "activated item not in user_profile items.."


def test_activate_item_already_activated():
    suffix = "double_activate_item"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)

    user_jwt_token = get_login_token(suffix)

    activate_item(client, activation_key, user_jwt_token)

    response_double_activation = activate_item(client, activation_key, user_jwt_token)

    assert response_double_activation.json()["detail"] == "item already activated.."


def test_activate_item_with_wrong_activation_key():
    suffix = "wrong_activation_key"

    activation_key = "wrong_activation_key"

    create_user_profile(client, suffix)

    user_jwt_token = get_login_token(suffix)

    response = activate_item(client, activation_key, user_jwt_token)

    assert response.json()["detail"] == f"wrong activation key {activation_key}.."
