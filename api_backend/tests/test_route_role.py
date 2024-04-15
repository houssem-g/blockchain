from fastapi.testclient import TestClient
from main import app

from app.db.setup_test import get_on_admin_token, get_simple_user_token

client = TestClient(app)


TEST_ROLE_NAME = "secret_agent"


def create_role(client: TestClient, suffix: str, jwt_token: str):
    response = client.post(
            "/v1/roles",
            headers={"Authorization": jwt_token},
            json={"role_name": f"{TEST_ROLE_NAME}_{suffix}"},
        )
    return response


def delete_role(client: TestClient, suffix: str, jwt_token: str):
    response = client.delete(
            f"/v1/roles/delete/{TEST_ROLE_NAME}_{suffix}",
            headers={"Authorization": jwt_token},
        )
    return response


def get_role(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/roles/{TEST_ROLE_NAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )
    return response


def test_on_admin_create_role():
    suffix = "on_admin_create_role"
    jwt_token = get_on_admin_token()
    response = create_role(client, suffix, jwt_token)
    assert response.status_code == 200, response
    assert response.json() == {"role_name": f"{TEST_ROLE_NAME}_{suffix}"}, "could not create a role"


def test_simple_user_create_role():
    suffix = "simple_user_create_role"
    jwt_token = get_simple_user_token()
    response = create_role(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == "you do not have the right to create a role"


def test_create_duplicate_role():
    suffix = "duplicate_role"
    jwt_token = get_on_admin_token()
    create_role(client, suffix, jwt_token)
    response = create_role(client, suffix, jwt_token)

    assert response.status_code == 200
    assert response.json()["detail"] == f"The role {TEST_ROLE_NAME}_{suffix} is already created"


def test_simple_user_delete_role():
    suffix = "simple_user_delete_role"
    jwt_token = get_simple_user_token()
    create_role(client, suffix, jwt_token)
    response = delete_role(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == 'you do not have the right to delete a role'


def test_on_admin_delete_role():
    suffix = "on_admin_delete_role"
    jwt_token = get_on_admin_token()
    create_role(client, suffix, jwt_token)
    response = delete_role(client, suffix, jwt_token)
    assert response.status_code == 200
    assert response.json() == f"The role {TEST_ROLE_NAME}_{suffix} is deleted!"


def test_get_role_from_name():
    suffix = "simple_user_get_role_from_name"
    simple_user_jwt_token = get_simple_user_token()
    on_admin_jwt_token = get_on_admin_token()
    create_role(client, suffix, on_admin_jwt_token)
    response = get_role(client, suffix, simple_user_jwt_token)
    assert response.status_code == 200
    assert response.json() == {"role_name": f"{TEST_ROLE_NAME}_{suffix}"}, "could not get one role"
