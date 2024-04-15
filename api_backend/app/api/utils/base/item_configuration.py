import json
from typing import Any, Union

from app.api.utils.base.brand import get_brand_from_name
from app.api.utils.base.item_class import get_item_class_from_product_number
from app.api.utils.item_config_utils import get_item_config_infos
from app.core.schemas.item_configuration import (ItemConfiguration,
                                                 ItemConfigurationDeletion)
from app.core.web3_utils.ipfs import (get_ipfs_config, upload_binary,
                                      upload_dict)
from app.db.models.item_configuration import ItemConfig
from fastapi import HTTPException
# from jose import JWTError, jwt  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def check_duplicate_item_conf(db: Session, item_class_id: int, description_json: object):
    existing_item_config: Union[None, ItemConfig] = (
        db.query(ItemConfig).filter(ItemConfig.item_class_id == item_class_id).filter(
            ItemConfig.description_json == description_json
        ).first()
    )
    if existing_item_config:
        print(f"we check if {description_json} is duplicated: {existing_item_config.description_json}")
    return bool(existing_item_config)


async def create_item_configuration(db: Session, item_conf: ItemConfiguration, image_binary: bytes):
    brand = await get_brand_from_name(db, item_conf.brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The brand {item_conf.brand_name} is not created, please create it first",
        )

    item_class = await get_item_class_from_product_number(db, item_conf.product_number, int(str(brand.brand_id)))
    if item_class is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The item class {item_conf.product_number} is not created, please create the item class first",
        )

    if await check_duplicate_item_conf(db, int(str(item_class.item_class_id)), item_conf.description_json) is True:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"Item config {item_conf.description_json} for PN {item_conf.product_number} is already registered",
        )

    ipfs_config = get_ipfs_config()

    image_hash_key, _, image_size = upload_binary(image_binary, ipfs_config)

    if not image_size:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"image file could not be uploaded hash: {image_hash_key}",
        )

    properties_json: Any = item_conf.description_json
    dict_description_json = (
        json.loads(properties_json)
        if isinstance(properties_json, str) or isinstance(properties_json, bytes)
        else properties_json
    )
    properties_json = (
        json.loads(properties_json)
        if isinstance(properties_json, str) or isinstance(properties_json, bytes)
        else properties_json
    )

    if not isinstance(properties_json, dict):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="properties dict could not be constructed",
        )

    properties_json["image"] = image_hash_key

    properties_hash_key = upload_dict(properties_json, ipfs_config)

    new_item_conf = ItemConfig(
        item_class_id=int(str(item_class.item_class_id)),
        image_hash=image_hash_key,
        properties_hash=properties_hash_key,
        description_json=dict_description_json,
    )

    db.add(new_item_conf)
    db.commit()
    db.refresh(new_item_conf)
    return new_item_conf, image_size


async def get_item_config_by_config_id(
    db: Session, item_config_id: int
) -> Union[ItemConfig, None]:
    item_config = (
        db.query(ItemConfig).filter(ItemConfig.item_config_id == item_config_id).first()
    )

    return item_config


async def get_item_config_by_description_json(
    db: Session, item_class_id: int, description_json: object
) -> Union[ItemConfig, None]:
    item_config = (
        db.query(ItemConfig).filter(
            ItemConfig.item_class_id == item_class_id and ItemConfig.description_json == description_json
        ).first()
    )

    return item_config


async def delete_item_config(db: Session, product_number: str, description_json: object, brand_name: str):

    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist..."
        )
    item_class = await get_item_class_from_product_number(db, product_number, int(str(brand.brand_id)))

    if item_class is None:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The item class with the PN {product_number} is not found")

    item_config = await get_item_config_by_description_json(db, int(str(item_class.item_class_id)), description_json)

    if item_config is None:
        raise HTTPException(status_code=HTTP_200_OK, detail="The item config is not found")

    item_config_info = await get_item_config_infos(db, item_config)
    item_config_deletion_info = ItemConfigurationDeletion(
        brand_name=str(item_config_info.brand_name),
        category_name=str(item_config_info.category_name),
        item_class_name=str(item_config_info.item_class_name),
        item_class_description=str(item_config_info.item_class_description),
        product_number=str(item_config_info.product_number),
        item_config_description=item_config_info.item_config_description,
        image_hash=str(item_config_info.image_hash),
        image_size=item_config_info.image_size,
        properties_hash=str(item_config_info.properties_hash),
        delete_status=True,
    )

    if isinstance(item_config, ItemConfig):
        db.delete(item_config)
        db.commit()
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The item config {description_json} is not found")
    return item_config_deletion_info
