from typing import List

import fastapi
from app.api.utils.base.brand import (create_brand, delete_brand,
                                      get_all_brands, get_brand_from_name)
from app.api.utils.base.user_profile import get_current_user_profile
from app.core.schemas.brand import BrandBase, BrandDeletion
from app.db.base import get_db
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.get("/v1/brands", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=List[BrandBase])
async def get_all_brands_route(db: Session = fastapi.Depends(get_db)):
    all_brands = await get_all_brands(db)
    return all_brands


@router.get(
    "/v1/brands/{brand_name}", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=BrandBase
)
async def get_brand_from_name_route(brand_name: str, db: Session = fastapi.Depends(get_db)):
    brand = await get_brand_from_name(db, brand_name)
    return brand


@router.post("/v1/brands", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=BrandBase)
async def create_brand_route(
    brand: BrandBase,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        brand = await create_brand(brand=brand, db=db)
        return brand

    else:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to create a brand")


@router.delete(
    "/v1/brands/delete/{brand_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=BrandDeletion,
)
async def delete_brand_route(
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        deleted_brand_str = await delete_brand(db=db, brand_name=brand_name)
        return deleted_brand_str
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to delete a brand")
