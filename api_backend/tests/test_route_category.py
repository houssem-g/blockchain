from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# to test item class we need to create here a category shoes
# then pls create here this category by runing only test_create_category
# with category name shoes

TEST_CATEGORY_NAME = "handbag"


def create_category(client: TestClient, suffix: str, jwt_token: str):
    response = client.post(
            "/v1/categories",
            headers={"Authorization": jwt_token},
            json={"category_name": f"{TEST_CATEGORY_NAME}_{suffix}"},
        )
    return response


def delete_category(client: TestClient, suffix: str, jwt_token: str):
    response = client.delete(
            f"/v1/categories/delete/{TEST_CATEGORY_NAME}_{suffix}",
            headers={"Authorization": jwt_token}
        )
    return response


def get_category(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/categories/{TEST_CATEGORY_NAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )
    return response


def test_simple_user_create_category():
    suffix = "simple_user_create_category"
    jwt_token = get_simple_user_token()
    response = create_category(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == "you do not have the right to create a category"


def test_on_admin_create_category():
    suffix = "on_admin_create_category"
    jwt_token = get_on_admin_token()
    response = create_category(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json() == {"category_name": f"{TEST_CATEGORY_NAME}_{suffix}"}


def test_create_duplicate_category():
    suffix = "duplicate_category"
    jwt_token = get_on_admin_token()
    create_category(client, suffix, jwt_token)
    response = create_category(client, suffix, jwt_token)

    assert response.status_code == 200
    assert response.json()["detail"] == f"The category {TEST_CATEGORY_NAME}_{suffix} is already created"


def test_simple_user_delete_category():
    suffix = "simple_user_delete_category"
    jwt_token = get_simple_user_token()
    create_category(client, suffix, jwt_token)
    response = delete_category(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to delete a category'


def test_on_admin_delete_category():
    suffix = "on_admin_delete_category"
    jwt_token = get_on_admin_token()
    create_category(client, suffix, jwt_token)
    response = delete_category(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["delete_status"]
    assert response.json()["category_name"] == f"{TEST_CATEGORY_NAME}_{suffix}"


def test_get_category_from_name():
    suffix = "simple_user_get_category_from_name"
    simple_user_jwt_token = get_simple_user_token()
    on_admin_jwt_token = get_on_admin_token()
    create_category(client, suffix, on_admin_jwt_token)
    response = get_category(client, suffix, simple_user_jwt_token)
    assert response.status_code == 200
    assert response.json() == {'category_name': f'{TEST_CATEGORY_NAME}_{suffix}'}
