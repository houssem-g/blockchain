from typing import Any, Dict, List

from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app
from tests.item.utils import (TEST_SERIAL_NUMBER, activate_item, create_item,
                              get_items_from_username, transfer_item)
from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_category import create_category
from tests.test_route_item_class import TEST_PN, create_item_class
from tests.test_route_item_config import create_item_config
from tests.test_route_user_profile import (DUMMY_USERNAME, create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)


def test_transfer_item_before_activation():
    suffix = "transfer_item_before_activation"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_user_profile(client, suffix)

    response = transfer_item(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert (
        response.json()["detail"] ==
        f"you cannot transfer item with SN {TEST_SERIAL_NUMBER}_{suffix} as you are not the owner"
    )


def test_transfer_item_as_on_admin():
    suffix = "transfer_item_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)
    owner_jwt_token = get_login_token(suffix)
    activate_item(client, activation_key, owner_jwt_token)

    transfer_response = transfer_item(client, suffix, on_admin_jwt)

    assert transfer_response.status_code == 200
    assert (
        transfer_response.json()["detail"] ==
        f"you cannot transfer item with SN {TEST_SERIAL_NUMBER}_{suffix} as you are not the owner"
    )


def test_transfer_item_as_owner():
    suffix = "transfer_item_as_owner"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)
    activate_item(client, activation_key, get_simple_user_token())

    transfer_response = transfer_item(client, suffix, get_simple_user_token())

    assert transfer_response.status_code == 200
    assert transfer_response.json()["transfered_to_username"] == f"{DUMMY_USERNAME}_{suffix}"
    assert transfer_response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"

    new_owner_items_response = get_items_from_username(client, suffix, on_admin_jwt)

    response_json: List[Dict[str, Any]] = new_owner_items_response.json()
    assert len(response_json) > 0, "no item was fetched.."


def test_transfer_item_as_brand_admin():
    suffix = "transfer_item_as_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]
    activate_item(client, activation_key, get_simple_user_token())

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")
    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix + "other")

    response = transfer_item(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert (
        response.json()["detail"] ==
        f"you cannot transfer item with SN {TEST_SERIAL_NUMBER}_{suffix} as you are not the owner"
    )


def test_transfer_item_as_other_user():
    suffix = "transfer_item_as_other_user"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]
    activate_item(client, activation_key, get_simple_user_token())

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")

    other_user_jwt = get_login_token(suffix + "other")

    transfer_response = transfer_item(client, suffix, other_user_jwt)

    assert transfer_response.status_code == 200
    assert (
        transfer_response.json()["detail"] ==
        f"you cannot transfer item with SN {TEST_SERIAL_NUMBER}_{suffix} as you are not the owner"
    )
