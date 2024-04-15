from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app
from tests.item.utils import (TEST_SERIAL_NUMBER, create_item,
                              create_items_list, delete_item)
from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_category import TEST_CATEGORY_NAME, create_category
from tests.test_route_item_class import (TEST_ITEM_CLASS_NAME, TEST_PN,
                                         create_item_class)
from tests.test_route_item_config import create_item_config
from tests.test_route_user_profile import (create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)


def test_create_item_as_on_admin():
    suffix = "create_item_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    response = create_item(client, suffix, test_description_json, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()["serial_number"] == f"{TEST_SERIAL_NUMBER}_{suffix}"
    assert response.json()["status"] == "not_activated"


def test_create_items_list_as_on_admin():
    suffix = "valid"
    test_description_json = '{"color": "blue", "size": "S"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    response = create_items_list(client, suffix, "valid_items.csv", on_admin_jwt)

    assert response.status_code == 200, response.json()
    assert len(response.json()) == 3, response.json()


def test_create_item_as_item_class_brand_admin():
    suffix = "create_item_as_correct_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    response = create_item(client, suffix, test_description_json, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json()["serial_number"] == f"{TEST_SERIAL_NUMBER}_{suffix}"
    assert response.json()["status"] == "not_activated"


def test_create_item_as_other_brand_admin():
    base_suffix = "create_item_as_other_brand_admin"
    item_brand_suffix = base_suffix + "_item_brand"
    other_brand_suffix = base_suffix + "_other_brand"
    test_description_json = '{"color": "red_' + item_brand_suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_category(client, item_brand_suffix, on_admin_jwt)
    create_brand(client, item_brand_suffix, on_admin_jwt)
    create_brand(client, other_brand_suffix, on_admin_jwt)
    create_item_class(client, item_brand_suffix, on_admin_jwt)
    create_item_config(client, item_brand_suffix, TEST_PN, test_description_json, on_admin_jwt)

    create_user_profile(client, base_suffix)
    make_user_admin_of_a_brand(client, base_suffix, on_admin_jwt, other_brand_suffix)

    brand_admin_jwt = get_login_token(base_suffix)

    response = create_item(client, item_brand_suffix, test_description_json, brand_admin_jwt)

    assert response.status_code == 200
    assert "you are not admin of the brand " in response.json().get('detail', "")


def test_create_item_as_simple_user():
    suffix = "create_item_as_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    response = create_item(client, suffix, test_description_json, get_simple_user_token())

    assert response.status_code == 200
    assert response.json().get("detail", "") == 'you do not have the right to create items..'


def test_create_item_with_no_created_item_class():
    suffix = "failed_create_item_1"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()
    create_brand(client, suffix, on_admin_jwt)

    response = create_item(client, suffix, test_description_json, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()["detail"] == f"This item class {TEST_PN}_{suffix} does not exist.."


def test_create_item_with_no_created_item_config():
    suffix = "failed_create_item_2"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    response = create_item(client, suffix, test_description_json, on_admin_jwt)

    assert response.status_code == 200
    assert (
        response.json()["detail"] == f"This item config {test_description_json} " +
        f"of the item class {TEST_PN}_{suffix} does not exist.."
    )


def test_duplicate_item():
    suffix = "duplicate_item"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)

    response = create_item(client, suffix, test_description_json, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()["detail"] == "This item is already registered"
    assert delete_item(client, suffix, on_admin_jwt).json()["delete_status"]


def test_create_item_with_same_brand_and_different_serial_number():
    suffix = "create_item_with_same_brand_and_different_serial_number"
    suffix_2 = "create_item_with_same_brand_and_different_serial_number_2"
    on_admin_jwt = get_on_admin_token()
    test_description_json = '{"color": "red_' + suffix + '"}'

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix_2, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, test_description_json, on_admin_jwt)
    response = create_item(client, suffix, on_admin_jwt, on_admin_jwt, serial_number=f"{TEST_SERIAL_NUMBER}_{suffix_2}")

    assert response.status_code == 200
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"
    assert response.json()["category_name"] == f"{TEST_CATEGORY_NAME}_{suffix}"
    assert response.json()["item_class_name"] == f"{TEST_ITEM_CLASS_NAME}_{suffix}"
    assert response.json()["item_class_description"] == "new item class for test"
    assert response.json()["product_number"] == f"{TEST_PN}_{suffix}"
    assert response.json()["serial_number"] == f"{TEST_SERIAL_NUMBER}_{suffix_2}"


def test_create_item_with_different_brand_and_same_serial_number():
    suffix = "create_item_with_different_brand_and_same_serial_number"
    suffix_2 = "create_item_with_different_brand_and_same_serial_number_2"
    test_description_json = '{"color": "red_' + suffix + '"}'
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_brand(client, suffix_2, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_category(client, suffix_2, on_admin_jwt)

    create_item_class(client, suffix, on_admin_jwt)
    create_item_class(client, suffix_2, on_admin_jwt)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    create_item_config(client, suffix_2, TEST_PN, test_description_json, on_admin_jwt)
    create_item(client, suffix, on_admin_jwt, on_admin_jwt)
    response = create_item(client, suffix_2, on_admin_jwt, on_admin_jwt, serial_number=f"{TEST_SERIAL_NUMBER}_{suffix}")

    assert response.status_code == 200
    print(response.json())
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix_2}"
    assert response.json()["category_name"] == f"{TEST_CATEGORY_NAME}_{suffix_2}"
    assert response.json()["item_class_name"] == f"{TEST_ITEM_CLASS_NAME}_{suffix_2}"
    assert response.json()["item_class_description"] == "new item class for test"
    assert response.json()["product_number"] == f"{TEST_PN}_{suffix_2}"
    assert response.json()["serial_number"] == f"{TEST_SERIAL_NUMBER}_{suffix}"
