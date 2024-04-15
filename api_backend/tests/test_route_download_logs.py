import io

import pandas as pd
from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app

from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_user_profile import (create_user_profile,
                                           get_login_token,
                                           make_user_admin_of_a_brand)

client = TestClient(app)


def get_csv_logs(client: TestClient, suffix: str, jwt_token: str):
    response = client.get(
        f"/v1/download_logs/{TEST_BRAND_NAME}_{suffix}",
        headers={"Authorization": jwt_token}
    )
    return response


def test_on_admin_download_logs():
    suffix = "on_admin_download_logs"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    response = get_csv_logs(client, suffix, jwt_token)
    assert response.status_code == 200
    df = pd.read_csv(io.StringIO(str(response.content, 'utf-8')))
    assert df.at[0, "route_url"] == "/v1/brands"
    assert df.at[0, "current_user_profile_id"] == 1


def test_brand_admin_download_logs():
    suffix = "brand_admin_from_brand_download_logs"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    create_user_profile(client, suffix)
    make_user_admin_of_a_brand(client, suffix, jwt_token)

    brand_admin_jwt = get_login_token(suffix)
    response = get_csv_logs(client, suffix, brand_admin_jwt)
    assert response.status_code == 200
    df = pd.read_csv(io.StringIO(str(response.content, 'utf-8')))
    assert df.at[0, "route_url"] == "/v1/brands"
    assert df.at[1, "route_url"] == "/v1/users/dummy_brand_admin_from_brand_download_logs/make_business_admin" \
        "/rolex_test_brand_admin_from_brand_download_logs"
    assert df.at[0, "current_user_profile_id"] == 1
    assert df.at[1, "current_user_profile_id"] == 1


def test_brand_admin_from_other_brand_download_logs():
    suffix = "brand_admin_from_other_brand_download_logs"
    suffix_other = "other_brand_download_logs"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    create_brand(client, suffix_other, jwt_token)
    create_user_profile(client, suffix_other)
    make_user_admin_of_a_brand(client, suffix_other, jwt_token)

    brand_admin_jwt = get_login_token(suffix_other)
    response = get_csv_logs(client, suffix, brand_admin_jwt)
    assert response.status_code == 200
    assert response.json()["detail"] == f"you are not admin of the brand {TEST_BRAND_NAME}_{suffix}"


def test_simple_user_download_logs():
    suffix = "simple_user_download_logs"
    jwt_token = get_on_admin_token()
    create_brand(client, suffix, jwt_token)
    simple_user_jwt_token = get_simple_user_token()
    response = get_csv_logs(client, suffix, simple_user_jwt_token)
    assert response.status_code == 200
    assert response.json()["detail"] == "you do not have the right to download logs..."
