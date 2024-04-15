from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TEST_BRAND_NAME = "rolex_test"


def create_brand(client: TestClient, suffix: str, jwt_token: str):
    response = client.post(
            "/v1/brands",
            headers={"Authorization": jwt_token},
            json={
                "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
                "logo_url": "https://www.logo.com",
                "website": "https://www.rolex.com",
                "description": "description test",
            },
        )
    return response


def delete_brand(client: TestClient, suffix: str, jwt_token: str):
    response = client.delete(
            f"/v1/brands/delete/{TEST_BRAND_NAME}_{suffix}",
            headers={"Authorization": jwt_token},
        )
    return response


def get_brand(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/brands/{TEST_BRAND_NAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )
    return response


def test_on_admin_create_brand():
    suffix = "on_admin_create_brand"
    jwt_token = get_on_admin_token()
    response = create_brand(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json() == {
        "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
        "logo_url": "https://www.logo.com",
        "website": "https://www.rolex.com",
        "description": "description test",
    }, "could not create a brand"


def test_simple_user_create_brand():
    suffix = "simple_user_create_brand"
    jwt_token = get_simple_user_token()
    response = create_brand(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == "you do not have the right to create a brand"


def test_create_duplicate_brand():
    suffix = "duplicate_brand"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    response = create_brand(client, suffix, jwt_token)

    assert response.status_code == 200
    assert response.json()["detail"] == f"The brand {TEST_BRAND_NAME}_{suffix} is already created"


def test_simple_user_delete_brand():
    suffix = "simple_user_delete_brand"
    jwt_token = get_simple_user_token()
    create_brand(client, suffix, jwt_token)
    response = delete_brand(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to delete a brand'


def test_on_admin_delete_brand():
    suffix = "on_admin_delete_brand"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    response = delete_brand(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_get_brand_from_name():
    suffix = "simple_user_get_brand_from_name"
    simple_user_jwt_token = get_simple_user_token()
    on_admin_jwt_token = get_on_admin_token()
    create_brand(client, suffix, on_admin_jwt_token)
    response = get_brand(client, suffix, simple_user_jwt_token)
    assert response.status_code == 200
    assert response.json() == {
        "brand_name": f"{TEST_BRAND_NAME}_{suffix}",
        "logo_url": "https://www.logo.com",
        "website": "https://www.rolex.com",
        "description": "description test",
    }, "could not get one brand"
