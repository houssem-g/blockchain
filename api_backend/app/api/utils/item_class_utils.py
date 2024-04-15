from app.api.utils.base.brand import get_brand_from_id, get_brand_from_name
from app.api.utils.base.category import (get_category_by_id,
                                         get_category_by_name)
from app.core.schemas.item_class import ItemClassInfo, ItemClassInput
from app.db.models.item_class import ItemClass
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def check_duplicate_item_class(db: Session, product_number: str, brand_id: int):
    existing_item_class = db.query(ItemClass.item_class_id).filter(
        ItemClass.product_number == product_number, ItemClass.brand_id == brand_id
        ).first()
    return bool(existing_item_class)


async def create_item_class(db: Session, item_class: ItemClassInput):

    brand = await get_brand_from_name(db, item_class.brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The brand {item_class.brand_name} is not created, please create the brand first",
        )
    if await check_duplicate_item_class(db, item_class.product_number, int(str(brand.brand_id))) is True:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The item class with PN {item_class.product_number} for {brand.brand_name} is already registered",
        )
    category = await get_category_by_name(db, item_class.category_name)
    if category is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The category {item_class.category_name} is not created, please create the category first",
        )
    new_item_class = ItemClass(
        category_id=category.category_id,
        brand_id=brand.brand_id,
        product_number=item_class.product_number,
        name=item_class.name,
        description=item_class.description,
    )
    db.add(new_item_class)
    db.commit()
    db.refresh(new_item_class)
    return new_item_class


async def get_item_class_infos(db: Session, item_class: ItemClass):
    brand = await get_brand_from_id(db, int(str(item_class.brand_id)))
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand with id {item_class.brand_id} does not exist.."
        )
    category = await get_category_by_id(db, int(str(item_class.category_id)))

    if category is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"category with id {item_class.category_id} does not exist.."
        )

    item_config_info = ItemClassInfo(
        brand_name=str(brand.brand_name),
        category_name=str(category.category_name),
        name=str(item_class.name),
        description=str(item_class.description),
        product_number=str(item_class.product_number),
    )
    return item_config_info
