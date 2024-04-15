from typing import Any, Dict, List

import pytest
from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app
from tests.item.utils import (
    TEST_SERIAL_NUMBER, activate_item, create_item, get_items_from_brand_name,
    get_items_from_brand_name_with_PN_filter, get_items_from_username,
    get_items_qr_codes_from_brand_name,
    get_items_qr_codes_from_brand_name_with_PN_filter)
from tests.test_route_brand import create_brand
from tests.test_route_category import create_category
from tests.test_route_item_class import TEST_PN, create_item_class
from tests.test_route_item_config import create_item_config
from tests.test_route_user_profile import (create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)

# ### TEST GET ITEMS OF A BRAND ###############################


def test_get_all_items_of_a_brand_as_on_admin():
    suffix = "get_items_of_a_brand_as_on_admin"
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

    response = get_items_from_brand_name(client, suffix, on_admin_jwt)

    assert response.status_code == 200

    response_json: List[Dict[str, Any]] = response.json()
    assert len(response_json) > 0, "no item was fetched.."

    item_info = response_json[0]
    assert all(
        [key in item_info for key in [
            'brand_name', 'category_name',
            'item_class_name', 'item_class_description',
            'product_number', 'item_config_description',
            'serial_number', 'status'
        ]]
    ), f"missing key in {item_info.keys()}"
    assert item_info['serial_number'] == f"{TEST_SERIAL_NUMBER}_{suffix}", "Serial number does not match"
    assert item_info["status"] == "activated"


def test_get_all_items_of_a_brand_as_brand_admin():
    suffix = "get_items_of_a_brand_as_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")
    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt, suffix)

    brand_admin_jwt = get_login_token(suffix + "other")
    user_jwt_token = get_login_token(suffix)

    activate_item(client, activation_key, user_jwt_token)

    response = get_items_from_brand_name(client, suffix, brand_admin_jwt)

    assert response.status_code == 200

    response_json: List[Dict[str, Any]] = response.json()
    assert len(response_json) > 0, "no item was fetched.."

    item_info = response_json[0]
    assert all(
        [key in item_info for key in [
            'brand_name', 'category_name',
            'item_class_name', 'item_class_description',
            'product_number', 'item_config_description',
            'serial_number', 'status'
        ]]
    ), f"missing key in {item_info.keys()}"
    assert item_info['serial_number'] == f"{TEST_SERIAL_NUMBER}_{suffix}", "Serial number does not match"
    assert item_info["status"] == "activated"


def test_get_all_items_of_a_brand_as_other_brand_admin():
    suffix = "get_items_of_a_brand_as_other_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")
    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix + "other")
    user_jwt_token = get_login_token(suffix)

    activate_item(client, activation_key, user_jwt_token)

    response = get_items_from_brand_name(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'


def test_get_all_items_of_a_brand_as_simple_user():
    suffix = "get_items_of_a_brand_as_simple_user"
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

    response = get_items_from_brand_name(client, suffix, get_simple_user_token())

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'


def test_get_items_of_a_brand_qr_codes_as_on_admin():
    suffix = "get_items_of_a_brand_qr_codes_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    response = get_items_qr_codes_from_brand_name(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert len(response.content) > 0, "no qr code was fetched.."


def test_get_items_of_a_brand_qr_codes_as_brand_admin():
    suffix = "get_items_of_a_brand_qr_codes_as_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")
    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt, suffix)

    brand_admin_jwt = get_login_token(suffix + "other")

    response = get_items_qr_codes_from_brand_name(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert len(response.content) > 0, "no qr code was fetched.."


def test_get_items_of_a_brand_qr_codes_as_other_brand_admin():
    suffix = "get_items_of_a_brand_qr_codes_as_other_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")
    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix + "other")

    response = get_items_qr_codes_from_brand_name(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'


def test_get_items_of_a_brand_qr_codes_as_simple_user():
    suffix = "get_items_of_a_brand_qr_codes_as_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    response = get_items_qr_codes_from_brand_name(client, suffix, get_simple_user_token())

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'

# ### TEST GET ITEMS OF A BRAND WITH FILTER ON PRODUCT NUMBER ###


def test_get_items_of_a_brand_with_filter_on_product_number_as_on_admin():
    suffix = "get_items_of_a_brand_with_filter_on_product_number_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    response = get_items_from_brand_name_with_PN_filter(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert len(response.json()) == 1, "no item was fetched.."


def test_get_items_of_a_brand_with_filter_on_product_number_as_brand_admin():
    suffix = "get_items_of_a_brand_with_fltr_on_pn_as_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")

    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt, suffix)

    brand_admin_jwt = get_login_token(suffix + "other")

    response = get_items_from_brand_name_with_PN_filter(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert len(response.json()) == 1, "no item was fetched.."


def test_get_items_of_a_brand_with_filter_on_product_number_as_other_brand_admin():
    suffix = "get_items_of_brand_with_fltr_pn_as_otr_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")
    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix + "other")

    response = get_items_from_brand_name_with_PN_filter(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'


def test_get_items_of_a_brand_with_filter_on_product_number_as_simple_user():
    suffix = "get_items_of_a_brand_with_filter_on_product_number_as_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    create_user_profile(client, suffix)

    response = get_items_from_brand_name_with_PN_filter(client, suffix, get_simple_user_token())

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'


def test_get_items_qr_codes_of_a_brand_with_filter_on_product_number_as_on_admin():
    suffix = "get_items_qr_codes_of_a_brand_with_fltr_on_pn_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    response = get_items_qr_codes_from_brand_name_with_PN_filter(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert len(response.content) > 1, "no item was fetched.."


def test_get_items_qr_codes_of_a_brand_with_filter_on_product_number_as_brand_admin():
    suffix = "get_itms_qr_cods_of_brnd_w_fltr_on_pn_as_brnd_admn"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "other")

    make_user_admin_of_a_brand(client, suffix + "other", on_admin_jwt, suffix)

    brand_admin_jwt = get_login_token(suffix + "other")

    response = get_items_qr_codes_from_brand_name_with_PN_filter(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert len(response.content) > 1, "no item was fetched.."


def test_get_items_qr_codes_of_a_brand_with_filter_on_product_number_as_simple_user():
    suffix = "get_items_qr_codes_of_a_brand_with_fltr_on_pn_as_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'
    test_description_json_2 = '{"color": "blue_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix + "other", on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix + "other", TEST_PN + "other", test_description_json_2, on_admin_jwt)

    create_item(client, suffix, test_description_json, on_admin_jwt)
    create_item(client, suffix + "other", test_description_json_2, on_admin_jwt)

    create_user_profile(client, suffix)

    response = get_items_qr_codes_from_brand_name_with_PN_filter(client, suffix, get_simple_user_token())

    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to get the items of this brand..'

# ######################################################################################


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_class_as_on_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_class_as_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_class_as_other_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_class_as_simple_user():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_config_as_on_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_config_as_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_config_as_other_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_items_of_an_item_config_as_simple_user():
    pass


def test_get_all_items_of_a_user_as_on_admin():
    suffix = "get_items_of_a_user_as_on_admin"
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

    response = get_items_from_username(client, suffix, on_admin_jwt)

    assert response.status_code == 200

    response_json: List[Dict[str, Any]] = response.json()
    assert len(response_json) > 0, "no item was fetched.."

    item_info = response_json[0]
    assert all(
        [key in item_info for key in [
            'brand_name', 'category_name',
            'item_class_name', 'item_class_description',
            'product_number', 'item_config_description',
            'serial_number', 'status'
        ]]
    ), f"missing key in {item_info.keys()}"
    assert item_info['serial_number'] == f"{TEST_SERIAL_NUMBER}_{suffix}", "Serial number does not match"
    assert item_info["status"] == "activated"


def test_get_all_items_of_a_user_as_self():
    suffix = "get_items_of_a_user_as_self"
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

    response = get_items_from_username(client, suffix, user_jwt_token)

    assert response.status_code == 200

    response_json: List[Dict[str, Any]] = response.json()
    assert len(response_json) > 0, "no item was fetched.."

    item_info = response_json[0]
    assert all(
        [key in item_info for key in [
            'brand_name', 'category_name',
            'item_class_name', 'item_class_description',
            'product_number', 'item_config_description',
            'serial_number', 'status'
        ]]
    ), f"missing key in {item_info.keys()}"
    assert item_info['serial_number'] == f"{TEST_SERIAL_NUMBER}_{suffix}", "Serial number does not match"
    assert item_info["status"] == "activated"


def test_get_all_items_of_a_user_as_brand_admin():
    suffix = "get_items_of_a_user_as_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "_brand")
    make_user_admin_of_a_brand(client, suffix + "_brand", on_admin_jwt)

    user_jwt_token = get_login_token(suffix)
    activate_item(client, activation_key, user_jwt_token)

    brand_admin_token = get_login_token(suffix + "_brand")

    response = get_items_from_username(client, suffix, brand_admin_token)

    assert response.status_code == 200
    assert response.json()["detail"] == "you cannot get an the items of another user_profile.."


def test_get_all_items_of_a_user_as_other_user():
    suffix = "get_items_of_a_user_as_other"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    item_response = create_item(client, suffix, test_description_json, on_admin_jwt)
    activation_key = item_response.json()["activation_key"]

    create_user_profile(client, suffix)
    create_user_profile(client, suffix + "_other")

    user_jwt_token = get_login_token(suffix)
    activate_item(client, activation_key, user_jwt_token)

    other_token = get_login_token(suffix + "_other")

    response = get_items_from_username(client, suffix, other_token)

    assert response.status_code == 200
    assert response.json()["detail"] == "you cannot get an the items of another user_profile.."
