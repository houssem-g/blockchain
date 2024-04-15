from typing import List

import fastapi
from app.api.utils.base.category import (create_category, delete_category,
                                         get_all_categories,
                                         get_category_by_name)
from app.api.utils.base.user_profile import get_current_user_profile
from app.core.schemas.category import CategoryBase, CategoryDeletion
from app.db.base import get_db
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.get(
    "/v1/categories/", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=List[CategoryBase]
)
async def get_all_categories_route(db: Session = fastapi.Depends(get_db)):
    return await get_all_categories(db)


@router.get(
    "/v1/categories/{category_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=CategoryBase,
)
async def get_category_from_name_route(category_name: str, db: Session = fastapi.Depends(get_db)):
    return await get_category_by_name(db, category_name)


@router.post("/v1/categories", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=CategoryBase)
async def create_category_route(
    category: CategoryBase,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        new_category = await create_category(db=db, category_name=category.category_name)
        return new_category
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to create a category")


@router.delete(
    "/v1/categories/delete/{category_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=CategoryDeletion,
)
async def delete_category_route(
    category_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        deleted_category_str = await delete_category(db=db, category_name=category_name)
        return deleted_category_str
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to delete a category")
