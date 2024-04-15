import pytest
from app.core.schemas.user_profile import UserTypes
from app.db.table_manager import DB_MODELS, TableManager
from pydantic import EmailStr


@pytest.mark.asyncio
async def test_create_table():
    dummy_user_email = EmailStr("dummy@dummy.com")
    dummy_username = "dummy"
    dummy_password = "dummy"
    dummy_description = "dummy"
    tables_created, on_admin_user = await TableManager().create_all_tables(
        dummy_user_email, dummy_username, dummy_password, dummy_description
    )
    all_tables_name = sorted([model.__tablename__ for model in DB_MODELS])
    assert tables_created == f"Tables {all_tables_name} created with success!"
    assert on_admin_user.user_type == UserTypes.ON_ADMIN, "on_admin user_profile is not admin"
