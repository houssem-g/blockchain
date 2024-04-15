import asyncio
import os

from app.db.table_manager import TableManager
from pydantic import EmailStr

TEST_ON_ADMIN_USER_NAME = os.environ.get("USER_NAME", "test")
TEST_ON_ADMIN_PASSWORD = os.environ.get("PASSWORD", "testdb")
TEST_ON_ADMIN_EMAIL = f"{TEST_ON_ADMIN_USER_NAME}@on-limited.com"
TEST_ON_ADMIN_DESCRIPTION = "Admin manager"


async def create_db():

    print(f"creating super user_profile with email: {TEST_ON_ADMIN_EMAIL} and password: {TEST_ON_ADMIN_PASSWORD}")
    table_manager = TableManager()
    await table_manager.delete_all_tables()
    await table_manager.create_all_tables(
        EmailStr(TEST_ON_ADMIN_EMAIL), TEST_ON_ADMIN_USER_NAME, TEST_ON_ADMIN_PASSWORD, TEST_ON_ADMIN_DESCRIPTION
    )
    print(f"Tables created are: {table_manager.get_all_tables_names()}")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())


if __name__ == "__main__":
    main()
