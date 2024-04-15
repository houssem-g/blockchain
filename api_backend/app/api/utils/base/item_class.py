from typing import Union

from app.api.utils.item_class_utils import get_item_class_infos
from app.core.schemas.item_class import ItemClassDeletion
from app.db.models.item_class import ItemClass
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_item_class_by_name(db: Session, item_class_name: str) -> Union[None, ItemClass]:
    item_class = db.query(ItemClass).filter(ItemClass.name == item_class_name).first()
    return item_class


async def get_item_class_by_id(db: Session, item_class_id: int) -> Union[None, ItemClass]:
    item_class = db.query(ItemClass).filter(ItemClass.item_class_id == item_class_id).first()
    return item_class


async def get_item_class_from_product_number(db: Session, product_number: str, brand_id: int) -> Union[None, ItemClass]:
    item_class = (
        db.query(ItemClass).filter(ItemClass.product_number == product_number, ItemClass.brand_id == brand_id).first()
    )
    return item_class


async def delete_item_class(db: Session, item_class_name: str):

    item_class = await get_item_class_by_name(db, item_class_name)
    if item_class:
        db.delete(item_class)
        db.commit()
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The item class {item_class_name} is not found")

    item_class_info = await get_item_class_infos(db, item_class)
    return ItemClassDeletion(
        product_number=item_class_info.product_number,
        name=item_class_info.name,
        description=item_class_info.description,
        category_name=item_class_info.category_name,
        brand_name=item_class_info.brand_name,
        delete_status=True,
    )
