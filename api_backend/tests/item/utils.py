
import os

from fastapi.testclient import TestClient
from tests.test_route_brand import TEST_BRAND_NAME
from tests.test_route_item_class import TEST_PN
from tests.test_route_user_profile import DUMMY_USERNAME

ITEMS_CSVS_PATH = "tests/samples/items"
TEST_SERIAL_NUMBER = "SN_123"


def delete_item(client: TestClient, suffix: str, jwt_token: str):
    response = client.delete(
        f"/v1/items/delete/{TEST_BRAND_NAME}_{suffix}/{TEST_SERIAL_NUMBER}_{suffix}",
        headers={"Authorization": jwt_token},
    )
    return response


def create_item(
    client: TestClient, suffix: str, description_json: str, jwt_token: str, serial_number: str = TEST_SERIAL_NUMBER
):
    if serial_number == TEST_SERIAL_NUMBER:
        serial_number = f"{TEST_SERIAL_NUMBER}_{suffix}"
    response = client.post(
        "/v1/items/create",
        headers={"Authorization": jwt_token},
        data={
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
            "serial_number": f"{serial_number}",
            "product_number": f"{TEST_PN}_{suffix}",
            "config_decription_json": description_json,
        },
    )
    return response


def create_items_list(client: TestClient, suffix: str, csv_file_name: str, jwt_token: str):
    with open(os.path.join(ITEMS_CSVS_PATH, csv_file_name), "rb") as f:
        csv_data = f.read()

    response = client.post(
        "/v1/items/create/list",
        headers={"Authorization": jwt_token},
        files={"items_csv": (csv_file_name, csv_data, "multipart/form-data")},
        data={"brand_name": f"{TEST_BRAND_NAME}_{suffix}"}
    )
    return response


def activate_item(client: TestClient, activation_key: str, jwt_token: str):
    response = client.post(
        "/v1/items/activate",
        headers={"Authorization": jwt_token},
        data={
            "activation_key": activation_key,
        },
    )
    return response


def transfer_item(client: TestClient, suffix: str, jwt_token: str):
    response = client.post(
        "/v1/items/transfer",
        headers={"Authorization": jwt_token},
        data={
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
            "serial_number": f"{TEST_SERIAL_NUMBER}_{suffix}",
            "username": f"{DUMMY_USERNAME}_{suffix}"
        }
    )
    return response


def burn_item(client: TestClient, suffix: str, jwt_token: str):
    response = client.post(
        "/v1/items/burn",
        headers={"Authorization": jwt_token},
        data={
            "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
            "serial_number": f"{TEST_SERIAL_NUMBER}_{suffix}"
        }
    )
    return response


def get_items_from_username(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/users/{DUMMY_USERNAME}_{suffix}/items",
        headers={"Authorization": jwt_token},
    )
    return response


def get_items_from_brand_name(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/brands/{TEST_BRAND_NAME}_{suffix}/items",
        headers={"Authorization": jwt_token},
    )
    return response


def get_items_qr_codes_from_brand_name(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/brands/{TEST_BRAND_NAME}_{suffix}/items/qr_codes",
        headers={"Authorization": jwt_token},
    )
    return response


def get_items_from_brand_name_with_PN_filter(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/brands/{TEST_BRAND_NAME}_{suffix}/items/{TEST_PN}_{suffix}",
        headers={"Authorization": jwt_token},
    )
    return response


def get_items_qr_codes_from_brand_name_with_PN_filter(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/brands/{TEST_BRAND_NAME}_{suffix}/items/{TEST_PN}_{suffix}/qr_codes",
        headers={"Authorization": jwt_token},
    )
    return response
