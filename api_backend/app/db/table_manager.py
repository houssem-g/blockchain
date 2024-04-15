
from typing import List, Union

from app.api.utils.base.user_profile import create_new_user_profile
from app.core.schemas.user_profile import UserProfileCreate
from app.db.base import Base, SessionLocal, engine
from app.db.models import DB_MODELS
from pydantic import EmailStr
from sqlalchemy import inspect  # type: ignore
from sqlalchemy.engine.reflection import Inspector  # type: ignore
from sqlalchemy.schema import (DropConstraint, DropTable,  # type: ignore
                               ForeignKeyConstraint, MetaData, Table)


class TableManager:
    """
    This class is to manage the tables in our DB by doing action like create, delete or check
    """

    def __init__(self) -> None:
        """
        Args:
            table (_type_): the name of table
            tableModel (_type_): the model created for this table
        """
        print(f"[TableManager] we have {len(DB_MODELS)} tables")
        self.session = SessionLocal

    async def create_all_tables(
            self, on_admin_email: EmailStr,
            on_admin_username: str,
            on_admin_password: str,
            on_admin_description: str,
            ):
        """create table on DB

        Args:
            table (string): this is the name of table that we are going to create
            tableModel (string): the model associated to the table
        """
        Base.metadata.create_all(bind=engine)
        self.session.commit()
        self.session.close()

        all_tables = sorted(self.get_all_tables_names())

        on_admin_user = UserProfileCreate(
            email=on_admin_email,
            username=on_admin_username,
            password=on_admin_password,
        )
        response = await create_new_user_profile(
            self.session, on_admin_user, on_admin_flag=True, require_email_confirmation=False
        )

        return f"Tables {all_tables} created with success!", response

    async def delete_all_tables(self):
        connection = engine.connect()
        transaction = connection.begin()
        inspector: Inspector = inspect(engine)

        # We need to re-create a minimal metadata with only the required things to
        # successfully emit drop constraints and tables commands for postgres (based
        # on the actual schema of the running instance)
        meta = MetaData()
        tables = []
        all_fkeys = []

        for table_name in inspector.get_table_names():
            fkeys = []

            for fkey in inspector.get_foreign_keys(table_name):
                if not fkey["name"]:
                    continue

                fkeys.append(ForeignKeyConstraint((), (), name=fkey["name"]))

            tables.append(Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)

        for fkey in all_fkeys:
            connection.execute(DropConstraint(fkey))

        for table in tables:
            connection.execute(DropTable(table))

        transaction.commit()

    def get_all_tables_names(self):
        list_tables_in_db: List[str] = []
        metadata = MetaData()
        metadata.reflect(bind=engine)
        for tab in metadata.sorted_tables:
            list_tables_in_db.append(str(tab))

        return list_tables_in_db

    def get_table(self, table_name) -> Union[Table, None]:

        metadata = MetaData()
        metadata.reflect(bind=engine)
        for tab in metadata.sorted_tables:
            if str(tab) == table_name:
                return tab

        return None

    async def create_simple_user(self, user_email: EmailStr, user_username: str, user_password: str):

        user_profile_create = UserProfileCreate(
            email=user_email,
            username=user_username,
            password=user_password,
        )

        response = await create_new_user_profile(
            self.session, user_profile_create, on_admin_flag=False, require_email_confirmation=False
        )

        return f"simple user_profile with username {user_username} created with success!", response
