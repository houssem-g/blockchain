from typing import List, Union

from app.core.schemas.brand import BrandBase, BrandDeletion
from app.db.models.brand import Brand
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_brand_from_id(db: Session, brand_id: int) -> Union[Brand, None]:
    res = db.query(Brand).filter(Brand.brand_id == brand_id).first()
    return res


async def get_all_brands(db: Session) -> List[Brand]:
    res = db.query(Brand).all()
    return res


async def get_brand_from_name(db: Session, brand_name: str) -> Union[Brand, None]:
    response = db.query(Brand).filter(Brand.brand_name == brand_name).first()
    return response


async def create_brand(brand: BrandBase, db: Session):
    if await get_brand_from_name(db, brand.brand_name) is not None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The brand {brand.brand_name} is already created",
        )
    brand = Brand(
        brand_name=brand.brand_name,
        logo_url=brand.logo_url,
        website=brand.website,
        description=brand.description,
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


async def delete_brand(db: Session, brand_name: str):

    brand = await get_brand_from_name(db, brand_name)
    if brand:
        db.delete(brand)
        db.commit()
        db.close()
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The brand {brand_name} is not found")

    return BrandDeletion(
        brand_name=str(brand.brand_name),
        logo_url=str(brand.logo_url),
        website=str(brand.website),
        description=str(brand.description),
        delete_status=True,
    )
