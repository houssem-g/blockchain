import io
from typing import Any, Dict, List, Union

import qrcode  # type: ignore
from app.api.utils.base.brand import get_brand_from_id, get_brand_from_name
from app.api.utils.base.category import get_category_by_id
from app.api.utils.base.item_class import get_item_class_by_id
from app.api.utils.base.item_configuration import get_item_config_by_config_id
from app.core.file_management_utils import zip_files
from app.core.schemas.item import ItemInfo
from app.db.models.item import Item
from app.db.models.item_class import ItemClass
from app.db.models.item_configuration import ItemConfig
from app.db.settings import settings
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from qrcode.image.base import BaseImage  # type: ignore
from qrcode.image.pil import PilImage  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_qr_codes_from_items_infos_in_a_zip_file(
    items_infos: List[ItemInfo], item_class_names: Union[List[str], None] = None
) -> StreamingResponse:
    """
    description: get a zip file with all the qr codes from a list of items info
    :param items_info: list of items info
    :return: zip file with all the qr codes
    """
    items_qr_codes_images: List[Dict[str, Any]] = []

    for item_info in items_infos:
        qr_code_string = f"{settings.frontend_URI}/activate#{item_info.activation_key}"

        item_image: Union[PilImage, BaseImage] = qrcode.make(qr_code_string)
        if not isinstance(item_image, PilImage):
            raise HTTPException(
                status_code=HTTP_200_OK, detail="qr code image is not a PIL image.."
            )

        img_byte_arr = io.BytesIO()

        item_image.save(img_byte_arr, format='PNG')

        image_dict = {"name": item_info.activation_key, "data": img_byte_arr.getvalue(), "extension": "png"}
        image_meta_data_dict = {
            "name": item_info.activation_key, "data": str.encode(item_info.__str__()), "extension": "txt"
        }
        items_qr_codes_images.extend([image_meta_data_dict, image_dict])

    zip_filename = "activation_qr_codes"

    zip_file = zip_files(items_qr_codes_images, zip_filename)

    return StreamingResponse(
        iter([zip_file]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename={zip_filename}"}
    )


async def get_item_infos(db: Session, item: Item):
    item_config = await get_item_config_by_config_id(db, int(str(item.item_configuration_id)))

    if item_config is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"item config {item.item_configuration_id} does not exist.."
        )

    item_class = await get_item_class_by_id(db, int(str(item_config.item_class_id)))
    if item_class is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"item class with id {item_config.item_class_id} does not exist.."
        )
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

    item_config_description: List[Dict[str, str]] = [
        {"key": key, "value": value} for key, value in item_config.description_json.items()
    ]

    item_info = ItemInfo(
        brand_name=str(brand.brand_name),
        category_name=str(category.category_name),
        item_class_name=str(item_class.name),
        item_class_description=str(item_class.description),
        product_number=str(item_class.product_number),
        activation_key=str(item.activation_key),
        item_config_description=item_config_description,
        image_hash_key=str(item_config.image_hash),
        serial_number=str(item.serial_number),
        status=str(item.status._value_)
    )
    return item_info


async def get_items_infos(db: Session, items_list: List[Item]):
    """
    description: get all the items infos from a list of items
    :param db: database session
    :param items_list: list of items
    :return: list of all the items infos
    """
    all_items_infos_list: List[ItemInfo] = []

    for item in items_list:
        item_info = await get_item_infos(db, item)
        all_items_infos_list.append(item_info)

    return all_items_infos_list


async def get_items_from_brand_name(db: Session, brand_name: str) -> List[Item]:
    """
    description: get all the items from a brand name
    :param db: database session
    :param brand_name: brand name
    :return: list of items
    """
    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist.."
            )

    # TODO: add big number query protection
    item_classes: List[ItemClass] = db.query(ItemClass).filter(ItemClass.brand_id == brand.brand_id).all()

    items: List[Item] = []

    for item_class in item_classes:
        current_item_class_configs: List[ItemConfig] = db.query(ItemConfig).filter(
            ItemConfig.item_class_id == item_class.item_class_id
        ).all()

        for item_config in current_item_class_configs:
            current_items: List[Item] = db.query(Item).filter(
                Item.item_configuration_id == item_config.item_config_id
            ).all()
            items.extend(current_items)

    return items
