import os
import time
from typing import Dict

import pytest
from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app

from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_category import create_category
from tests.test_route_item_class import TEST_PN, create_item_class
from tests.test_route_user_profile import (create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)
sample_image = "tests/samples/sample_1.jpg"
valid_configs_path = "tests/samples/item_configs/"
config_images_names = ["blue.jpg", "green.jpg"]


# TODO: add deletion of corresponding items when deleting a config


def create_item_config(client: TestClient, suffix: str, pn: str, test_description_json: str, jwt_token: str):
    with open(sample_image, "rb") as f:
        image_data = f.read()
    assert len(image_data) > 0
    response = client.post(
        "/v1/items_configs",
        headers={"Authorization": jwt_token},
        data={
            "product_number": f"{pn}_{suffix}",
            "description_json": test_description_json,
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
        },
        files={"image": ("sample_1", image_data, "multipart/form-data")},
    )
    return response


def create_item_configs_list(
    client: TestClient, suffix: str, jwt_token: str
):
    with open(os.path.join(valid_configs_path, "valid_configs.csv"), "rb") as f:
        csv_data = f.read()

    config_images_bytes_dict: Dict[str, bytes] = {}

    for image_name in config_images_names:
        with open(os.path.join(valid_configs_path, image_name), "rb") as f:
            config_images_bytes_dict[image_name] = f.read()

    files = [("item_configs_csv", ("valid_configs", csv_data, "multipart/form-data"))]

    files.extend(
        [
            ("images", (image_name, config_images_bytes_dict[image_name], "multipart/form-data"))
            for image_name in config_images_names
        ]
    )

    response = client.post(
        "/v1/items_configs/list",
        headers={"Authorization": jwt_token},
        data={"brand_name": f"{TEST_BRAND_NAME}_{suffix}"},
        files=files,
    )
    return response


def delete_item_config(client: TestClient, suffix: str, pn: str, test_description_json: str, jwt_token: str):
    response = client.delete(
        "/v1/items_configs/delete",
        headers={"Authorization": jwt_token},
        data={
            "product_number": f"{pn}_{suffix}",
            "description_json": test_description_json,
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}"},
    )
    return response


def get_item_config_img_from_hash(client: TestClient, hash_key: str, jwt_token: str):
    return client.get(
        f"/v1/imgs/{hash_key}",
        headers={"Authorization": jwt_token},
    )


def test_create_item_config_as_on_admin():
    suffix = "create_item_config_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    response = create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    assert response.status_code == 200
    assert response.json()["properties_hash"]
    assert response.json()["image_hash"]


def test_create_item_configs_list_as_on_admin():
    suffix = ""

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    response = create_item_configs_list(client, suffix, on_admin_jwt)

    assert response.status_code == 200, response.json()
    assert len(response.json()) == 3, response.json()
    assert response.json()[0]["image_size"] == 3095, response.json()
    assert len(response.json()[0].keys()) > 2, response.json()


def test_create_item_config_as_item_class_brand_admin():
    suffix = "create_item_config_as_correct_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    response = create_item_config(client, suffix, TEST_PN, test_description_json, brand_admin_jwt)

    assert response.status_code == 200
    assert response.json()["properties_hash"]
    assert response.json()["image_hash"]


def test_create_item_config_as_other_brand_admin():
    base_suffix = "create_item_config_as_other_brand_admin"
    item_config_brand_suffix = base_suffix + "_item_config_brand"
    other_brand_suffix = base_suffix + "_other_brand"
    test_description_json = '{"color": "red_' + item_config_brand_suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_category(client, item_config_brand_suffix, on_admin_jwt)
    create_brand(client, item_config_brand_suffix, on_admin_jwt)
    create_brand(client, other_brand_suffix, on_admin_jwt)
    create_item_class(client, item_config_brand_suffix, on_admin_jwt)

    create_user_profile(client, base_suffix)
    make_user_admin_of_a_brand(client, base_suffix, on_admin_jwt, other_brand_suffix)

    brand_admin_jwt = get_login_token(base_suffix)

    response = create_item_config(client, item_config_brand_suffix, TEST_PN, test_description_json, brand_admin_jwt)

    assert response.status_code == 200
    assert "you are not admin of the brand " in response.json().get('detail', "")


def test_create_item_config_as_simple_user():
    suffix = "create_item_config_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    response = create_item_config(client, suffix, TEST_PN, test_description_json, get_simple_user_token())

    assert response.status_code == 200
    assert response.json().get("detail", "") == 'you do not have the right to create item configs..'


def test_delete_item_config_as_on_admin():
    suffix = "del_item_config_as_on_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'
    response_description_json = "{'color': 'red_" + suffix + "'}"

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    response = delete_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_delete_item_config_as_item_conf_brand_admin():
    suffix = "del_item_config_as_item_conf_brand_admin"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, on_admin_jwt)

    brand_admin_jwt = get_login_token(suffix)

    create_item_config(client, suffix, TEST_PN, test_description_json, brand_admin_jwt)

    response = delete_item_config(client, suffix, TEST_PN, test_description_json, brand_admin_jwt)
    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_delete_item_config_as_other_brand_admin():
    base_suffix = "del_item_config"
    item_class_brand_suffix = base_suffix + "_item_class_brand"
    other_brand_suffix = base_suffix + "_other_brand"

    test_description_json = '{"color": "red_' + item_class_brand_suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, item_class_brand_suffix, on_admin_jwt)
    create_brand(client, other_brand_suffix, on_admin_jwt)
    create_category(client, item_class_brand_suffix, on_admin_jwt)
    create_item_class(client, item_class_brand_suffix, on_admin_jwt)

    create_user_profile(client, base_suffix)
    make_user_admin_of_a_brand(client, base_suffix, on_admin_jwt, other_brand_suffix)

    brand_admin_jwt = get_login_token(base_suffix)

    create_item_config(client, item_class_brand_suffix, TEST_PN, test_description_json, brand_admin_jwt)

    response = delete_item_config(client, item_class_brand_suffix, TEST_PN, test_description_json, brand_admin_jwt)
    assert response.status_code == 200
    assert "you are not admin of the brand " in response.json()['detail']


def test_delete_item_config_as_simple_user():
    suffix = "del_item_config_as_simple_user"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    response = delete_item_config(client, suffix, TEST_PN, test_description_json, get_simple_user_token())
    assert response.status_code == 200
    assert response.json()['detail'] == 'you do not have the right to delete item classes..'


def test_duplicate_items_configs():
    suffix = "test_duplicate_item_config"
    test_description_json = '{"color": "red_' + suffix + '"}'
    on_admin_jwt = get_on_admin_token()
    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)
    time.sleep(0.1)
    create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    response = create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)
    assert response.status_code == 200
    assert (
        response.json()["detail"] == f"Item config {test_description_json} for" +
        f" PN {TEST_PN}_{suffix} is already registered"
    )


def test_item_class_not_created():
    no_existing_pn = "abc123_456-789"
    suffix = "create_item_config2"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    response = create_item_config(client, suffix, no_existing_pn, test_description_json, on_admin_jwt)
    assert response.status_code == 200
    assert (
        response.json()["detail"]
        == f"item class with product number {no_existing_pn}_{suffix} does not exist.."
    )


@pytest.mark.skip("not written yet")
def test_get_all_item_configs_of_an_item_class_as_on_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_configs_of_an_item_class_as_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_configs_of_an_item_class_as_other_brand_admin():
    pass


@pytest.mark.skip("not written yet")
def test_get_all_item_configs_of_an_item_class_as_simple_user():
    pass


def test_route_get_imgs_path():
    suffix = "get_imgs_from_hash"
    test_description_json = '{"color": "red_' + suffix + '"}'

    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)
    create_category(client, suffix, on_admin_jwt)
    create_item_class(client, suffix, on_admin_jwt)

    item_config_resp = create_item_config(client, suffix, TEST_PN, test_description_json, on_admin_jwt)

    with open(sample_image, "rb") as f:
        image_data = f.read()

    resp = get_item_config_img_from_hash(client, item_config_resp.json()["image_hash"], on_admin_jwt)

    assert image_data == resp.content, resp.content
