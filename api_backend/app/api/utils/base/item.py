import secrets
from typing import List, Union

from app.api.utils.base.item_class import (get_item_class_by_id,
                                           get_item_class_from_product_number)
from app.api.utils.base.item_configuration import (
    get_item_config_by_config_id, get_item_config_by_description_json)
from app.api.utils.base.user_profile import get_user_profile_by_username
from app.core.schemas.item import ItemCreation, ItemStatus
from app.db.models.item import Item
from app.db.models.item_configuration import ItemConfig
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_item_by_serial_number(db: Session, serial_number: str, brand_id: int) -> Union[Item, None]:
    items: List[Item] = db.query(Item).filter(Item.serial_number == serial_number).all()
    for item in items:
        item_config = await get_item_config_by_config_id(db, int(str(item.item_configuration_id)))
        item_class = await get_item_class_by_id(db, int(str(item_config.item_class_id))) if item_config else None
        if item_class and (int(str(item_class.brand_id)) == brand_id):
            return item
    return None


async def get_item_by_activation_key(db: Session, activation_key: str) -> Union[Item, None]:
    item = db.query(Item).filter(Item.activation_key == activation_key).first()
    return item


async def get_items_of_username(db: Session, username: str) -> List[Item]:
    user_profile = await get_user_profile_by_username(db=db, username=username)
    if user_profile is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"username {username} does not exist.."
            )
    items: List[Item] = db.query(Item).filter(Item.user_profile_id == user_profile.user_profile_id).limit(1000).all()
    # TODO: replace this type of query with a window range query.
    # See: https://github.com/sqlalchemy/sqlalchemy/wiki/RangeQuery-and-WindowedRangeQuery
    if len(items) == 0:
        return []
    return items


async def transfer_item_to_username(db: Session, serial_number: str, username: str, brand_id: int):
    item = await get_item_by_serial_number(db=db, serial_number=serial_number, brand_id=brand_id)

    if item is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail="you cannot transfer an item you do not own.."
            )

    if item.status == ItemStatus.NOT_ACTIVATED:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"you cannot transfer item with SN {serial_number} as it is not activated yet.."
        )
    user_profile = await get_user_profile_by_username(db=db, username=username)
    if user_profile is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"username {username} does not exist.."
            )
    item.user_profile_id = user_profile.user_profile_id
    db.commit()
    db.refresh(item)
    return item


async def activate_item(db: Session, activation_key: str, current_user_profile_id: int):
    item = await get_item_by_activation_key(db=db, activation_key=activation_key)

    if item is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"wrong activation key {activation_key}.."
            )

    if item.status != ItemStatus.NOT_ACTIVATED:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="item already activated.."
        )

    item.__setattr__("user_profile_id", current_user_profile_id)
    item.__setattr__("status", ItemStatus.ACTIVATED)
    db.commit()
    db.refresh(item)
    return item


async def burn_item(db: Session, serial_number: str, brand_id: int):
    item = await get_item_by_serial_number(db=db, serial_number=serial_number, brand_id=brand_id)

    if item is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"wrong serial number {serial_number}.."
            )

    if item.status != ItemStatus.ACTIVATED:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="item can only be burned if in the activated status.."
        )

    item.__setattr__("user_profile_id", None)
    item.__setattr__("status", ItemStatus.BURNED)
    db.commit()
    db.refresh(item)
    return item


async def check_duplicate_item(db: Session, serial_number: str, brand_id: int):
    existing_item: List[Item] = db.query(Item).filter(Item.serial_number == serial_number).all()
    for item in existing_item:
        item_config = await get_item_config_by_config_id(db, int(str(item.item_configuration_id)))
        item_class = await get_item_class_by_id(db, int(str(item_config.item_class_id))) if item_config else None
        if item_class and (int(str(item_class.brand_id)) == brand_id):
            return True
    return False


async def create_item(db: Session, item: ItemCreation, brand_id: int):
    item_class = await get_item_class_from_product_number(db, item.product_number, brand_id)
    if not item_class:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"This item class {item.product_number} does not exist..",
        )

    if await check_duplicate_item(db, item.serial_number, int(str(item_class.brand_id))) is True:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="This item is already registered",
        )

    item_config = await get_item_config_by_description_json(
        db, int(str(item_class.item_class_id)), item.config_decription_json
    )
    if not isinstance(item_config, ItemConfig):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"This item config {item.config_decription_json} " +
            f"of the item class {item.product_number} does not exist..",
        )

    new_item = Item(
        item_configuration_id=item_config.item_config_id,
        serial_number=item.serial_number,
        status=ItemStatus.NOT_ACTIVATED,
        activation_key=secrets.token_hex(5)
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


async def delete_item(db: Session, serial_number: str, brand_id: int):

    item = await get_item_by_serial_number(db, serial_number, brand_id)
    if item:
        db.delete(item)
        db.commit()
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The item {serial_number} is not found")
    return item
