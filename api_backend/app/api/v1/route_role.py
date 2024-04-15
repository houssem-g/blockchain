from typing import List

import fastapi
from app.api.utils.base.role import (create_role, delete_role, get_all_roles,
                                     get_role_by_name)
from app.api.utils.base.user_profile import get_current_user_profile
from app.core.schemas.role import Role
from app.db.base import get_db
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.get("/v1/roles/", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=List[Role])
async def get_all_roles_route(db: Session = fastapi.Depends(get_db)):
    results = await get_all_roles(db)
    if results is None:
        return []
    return results


@router.get("/v1/roles/{role_name}", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=Role)
async def get_role_from_name(role_name: str, db: Session = fastapi.Depends(get_db)):
    return await get_role_by_name(db, role_name)


@router.post("/v1/roles", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=Role)
async def create_role_route(
    role: Role,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        new_role = await create_role(db=db, role_name=role.role_name)
        return new_role
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to create a role")


@router.delete("/v1/roles/delete/{role_name}", dependencies=[fastapi.Depends(get_current_user_profile)])
async def delete_role_route(
    role_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        deleted_role = await delete_role(db=db, role_name=role_name)
        return deleted_role
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to delete a role")
