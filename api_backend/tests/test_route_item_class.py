import os

import pytest
from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app

from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_category import TEST_CATEGORY_NAME, create_category
from tests.test_route_user_profile import (create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)

TEST_PN = "PN-00001"
TEST_ITEM_CLASS_NAME = "newlife"
TEST_ITEM_CLASS_DESC = "new item class for test"
ITEM_CLASSES_CSVS_PATH = "tests/samples/item_classes"


def create_item_class(client: TestClient, suffix: str, jwt_token: str, product_number: str = TEST_PN):
    if product_number == TEST_PN:
        product_number = f"{TEST_PN}_{suffix}"
    response = client.post(
        "/v1/items_classes",
        headers={"Authorization": jwt_token},
        json={
            "category_name": f"{TEST_CATEGORY_NAME}_{suffix}",
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
            "product_number": product_number,
            "name": f"{TEST_ITEM_CLASS_NAME}_{suffix}",
            "description": TEST_ITEM_CLASS_DESC,
        },
    )
    return response


def create_item_classes_list(
    client: TestClient, csv_file_name: str, jwt_token: str
):
    with open(os.path.join(ITEM_CLASSES_CSVS_PATH, csv_file_name), "rb") as f:
        csv_data = f.read()
    response = client.post(
        "/v1/items_classes/list",
        headers={"Authorization": jwt_token},
        files={"item_classes_csv": (csv_file_name, csv_data, "multipart/form-data")}
    )
    return response


def delete_item_class(client: TestClient, suffix: str, jwt_token: str):
    response = client.delete(
        f"/v1/items_classes/delete/{TEST_ITEM_CLASS_NAME}_{suffix}",
        headers={"Authorization": jwt_token},
    )
    return response


def test_create_items_class_as_on_admin():
    suffix = "create_item_class_as_on_admin"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    response = create_item_class(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert response.json() == {
        "product_number": f"{TEST_PN}_{suffix}",
        "name": f"{TEST_ITEM_CLASS_NAME}_{suffix}",
        "description": TEST_ITEM_CLASS_DESC,
        "category_name": f"{TEST_CATEGORY_NAME}_{suffix}",
        "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
    }


def test_create_items_class_as_item_class_brand_admin():
    suffix = "create_item_class_as_correct_brand_admin"

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    response = create_item_class(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json() == {
        "product_number": f"{TEST_PN}_{suffix}",
        "name": f"{TEST_ITEM_CLASS_NAME}_{suffix}",
        "description": TEST_ITEM_CLASS_DESC,
        "category_name": f"{TEST_CATEGORY_NAME}_{suffix}",
        "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
    }


def test_create_items_class_as_other_brand_admin():
    base_suffix = "create_item_class"
    item_class_brand_suffix = base_suffix + "_item_class_brand"
    other_brand_suffix = base_suffix + "_other_brand"

    on_admin_jwt = get_on_admin_token()

    create_category(client, item_class_brand_suffix, on_admin_jwt)
    create_brand(client, item_class_brand_suffix, on_admin_jwt)
    create_brand(client, other_brand_suffix, on_admin_jwt)

    create_user_profile(client, base_suffix)
    make_user_admin_of_a_brand(client, base_suffix, on_admin_jwt, other_brand_suffix)

    brand_admin_jwt = get_login_token(base_suffix)

    response = create_item_class(client, item_class_brand_suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert "you are not admin of the brand " in response.json()['detail']


def test_create_items_class_as_simple_user():
    suffix = "create_item_class_as_simple_user"
    on_admin_jwt = get_simple_user_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    response = create_item_class(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()['detail'] == 'you do not have the right to create item classes..'


def test_create_items_class_list_as_on_admin():
    suffix = "valid"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    response = create_item_classes_list(client, "valid_item_classes.csv", on_admin_jwt)

    assert response.status_code == 200, response.json()
    assert len(response.json()) == 2, response.json()


def test_create_items_class_list_as_on_admin_with_duplicate():
    suffix = "duplicate"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    response = create_item_classes_list(client, "item_classes_with_duplicates.csv", on_admin_jwt)

    assert response.status_code == 200, response.json()
    assert response.json()["detail"] == 'The item class with PN PN-00003 for rolex_test_duplicate is already registered'


def test_delete_item_class_as_on_admin():
    suffix = "del_item_class_as_on_admin"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    create_item_class(client, suffix, brand_admin_jwt)

    response = delete_item_class(client, suffix, on_admin_jwt)
    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_delete_item_class_as_item_class_brand_admin():
    suffix = "del_item_class_as_correct_brand_admin"

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    create_item_class(client, suffix, brand_admin_jwt)

    response = delete_item_class(client, suffix, brand_admin_jwt)
    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_delete_item_class_as_other_brand_admin():
    base_suffix = "del_item_class"
    item_class_brand_suffix = base_suffix + "_item_class_brand"
    other_brand_suffix = base_suffix + "_other_brand"

    on_admin_jwt = get_on_admin_token()

    create_category(client, item_class_brand_suffix, on_admin_jwt)
    create_brand(client, item_class_brand_suffix, on_admin_jwt)
    create_brand(client, other_brand_suffix, on_admin_jwt)

    create_user_profile(client, base_suffix)
    make_user_admin_of_a_brand(client, base_suffix, on_admin_jwt, other_brand_suffix)

    brand_admin_jwt = get_login_token(base_suffix)

    create_item_class(client, item_class_brand_suffix, on_admin_jwt)

    response = delete_item_class(client, item_class_brand_suffix, brand_admin_jwt)
    assert response.status_code == 200
    assert "you are not admin of the brand " in response.json()['detail']


def test_delete_item_class_as_simple_user():
    suffix = "del_item_class_as_simple_user"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    create_item_class(client, suffix, brand_admin_jwt)
    create_item_class(client, suffix, brand_admin_jwt)

    response = delete_item_class(client, suffix, get_simple_user_token())

    assert response.status_code == 200
    assert response.json()['detail'] == 'you do not have the right to delete item classes..'


def test_duplicate_items_classes():
    suffix = "dup_item_class"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    create_item_class(client, suffix, brand_admin_jwt)

    response = create_item_class(client, suffix, brand_admin_jwt)
    assert response.status_code == 200
    assert response.json()["detail"] == (f"The item class with PN {TEST_PN}_{suffix} for {TEST_BRAND_NAME}_{suffix}"
                                         " is already registered")


def test_brand_not_created():
    suffix = "brand_not_create_item_class"
    on_admin_jwt = get_on_admin_token()

    create_category(client, suffix, on_admin_jwt)

    response = create_item_class(client, suffix, on_admin_jwt)
    assert response.status_code == 200
    print(response.json())
    assert (
        response.json()["detail"]
        == f"The brand {TEST_BRAND_NAME}_{suffix} is not created, please create the brand first"
    )


def test_category_not_created():
    suffix = "cat_not_created_item_class"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    response = create_item_class(client, suffix, brand_admin_jwt)

    assert response.status_code == 200
    assert (
        response.json()["detail"]
        == f"The category {TEST_CATEGORY_NAME}_{suffix} is not created, please create the category first"
    )


def test_create_item_class_with_same_brand_and_same_product_number():
    suffix = "create_item_with_same_brand_and_same_product_number"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    create_item_class(client, suffix, on_admin_jwt)
    response = create_item_class(client, suffix, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()["detail"] == ("The item class with PN PN-00001_create_item_with_same_brand_and_"
                                         f"same_product_number for rolex_test_{suffix} is already registered")


def test_create_item_class_with_same_brand_and_different_product_number():
    suffix = "create_item_with_same_brand_and_different_product_number"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)

    create_item_class(client, suffix, on_admin_jwt)
    response = create_item_class(client, suffix, on_admin_jwt, product_number=f"PN-00002_{suffix}")

    assert response.status_code == 200
    assert response.json() == {
        "product_number": f"PN-00002_{suffix}",
        "name": f"{TEST_ITEM_CLASS_NAME}_{suffix}",
        "description": TEST_ITEM_CLASS_DESC,
        "category_name": f"{TEST_CATEGORY_NAME}_{suffix}",
        "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
    }


def test_create_item_class_with_different_brand_and_same_product_number():
    suffix = "create_item_with_different_brand_and_same_product_number"
    suffix_2 = "create_item_with_different_brand_and_same_product_number_2"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_brand(client, suffix_2, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_category(client, suffix_2, on_admin_jwt)

    create_item_class(client, suffix, on_admin_jwt)
    response = create_item_class(client, suffix_2, on_admin_jwt, product_number=f"PN-00001_{suffix}")

    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "product_number": f"PN-00001_{suffix}",
        "name": f"{TEST_ITEM_CLASS_NAME}_{suffix_2}",
        "description": TEST_ITEM_CLASS_DESC,
        "category_name": f"{TEST_CATEGORY_NAME}_{suffix_2}",
        "brand_name": f"{TEST_BRAND_NAME}_{suffix_2}",
    }


@pytest.mark.skip("not written yet")
def test_get_item_class_from_product_number_as_on_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_item_class_from_product_number_as_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_item_class_from_product_number_as_other_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_item_class_from_product_number_as_simple_user():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_classes_of_a_brand_as_on_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_classes_of_a_brand_as_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_classes_of_a_brand_as_other_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_classes_of_a_brand_as_simple_user():
    pass
