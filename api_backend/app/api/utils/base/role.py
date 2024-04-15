from typing import List, Union

from app.db.models.role import Role
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

BRAND_ROLE_NAMES_DICT = {"business_admin": "business_admin"}


async def get_all_roles(db: Session) -> List[Role]:
    return db.query(Role).all()


async def get_role_by_id(db: Session, role_id: int) -> Union[Role, None]:
    return db.query(Role).filter(Role.role_id == role_id).first()


async def get_role_by_name(db: Session, role_name: str) -> Union[Role, None]:
    return db.query(Role).filter(Role.role_name == role_name).first()


async def create_role(db: Session, role_name: str):
    if await get_role_by_name(db, role_name) is not None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The role {role_name} is already created",
        )
    role = Role(role_name=role_name)
    db.add(role)
    db.commit()
    db.refresh(role)
    role = db.query(Role).filter(Role.role_name == role_name).first()
    assert role is not None, f"could not create role {role_name}"
    return role


async def delete_role(db: Session, role_name: str):

    role = await get_role_by_name(db, role_name)
    if role:
        db.delete(role)
        db.commit()
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The role with the name {role_name} is not found")
    return f"The role {role_name} is deleted!"
