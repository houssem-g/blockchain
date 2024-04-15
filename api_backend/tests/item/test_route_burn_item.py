
from app.db.setup_test import get_on_admin_token, get_simple_user_token
from fastapi.testclient import TestClient
from main import app
from tests.item.utils import activate_item, burn_item, create_item
from tests.test_route_brand import TEST_BRAND_NAME, create_brand
from tests.test_route_category import create_category
from tests.test_route_item_class import TEST_PN, create_item_class
from tests.test_route_item_config import create_item_config
from tests.test_route_user_profile import create_user_profile, get_login_token

client = TestClient(app)


def test_burn_item_as_owner_user():
    suffix = "burn_item_owned"
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

    response = burn_item(client, suffix, user_jwt_token)

    assert response.json()["burn_status"]
    assert response.json()["delete_status"] is False
    assert response.json()["brand_name"] == f"{TEST_BRAND_NAME}_{suffix}"


def test_burn_item_as_other_user():
    suffix = "burn_item_not_owned"
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

    response = burn_item(client, suffix, get_simple_user_token())

    assert response.json()["detail"] == "you cannot burn an item you do not own.."


def test_burn_item_with_wrong_sn():
    suffix = "burn_item_that_doesnt_exist"
    on_admin_jwt = get_on_admin_token()

    create_brand(client, suffix, on_admin_jwt)

    response = burn_item(client, suffix, get_simple_user_token())

    assert response.json()["detail"] == "you cannot burn an item you do not own.."
