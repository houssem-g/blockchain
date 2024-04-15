import asyncio
import os

import psycopg2  # type: ignore
from app.db.settings import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # type: ignore

DB_NAME = os.environ.get("DB_NAME")


async def delete_tables_from_current_db():
    print("Deleting Database!")

    # Connect to PostgreSQL DBMS
    postgresConnection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user=settings.user_name,
        password=settings.password,
    )

    postgresConnection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Obtain a database Cursor
    cur_ob = postgresConnection.cursor()
    sqlRemDb = f"DROP database {DB_NAME};"
    cur_ob.execute(sqlRemDb)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_tables_from_current_db())


if __name__ == "__main__":
    main()
