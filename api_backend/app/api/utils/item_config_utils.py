from typing import Dict, List, Union

from app.api.utils.base.brand import get_brand_from_id
from app.api.utils.base.category import get_category_by_id
from app.api.utils.base.item_class import get_item_class_by_id
from app.core.schemas.item_configuration import ItemConfigurationInfo
from app.db.models.item_configuration import ItemConfig
from fastapi import HTTPException
# from jose import JWTError, jwt  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_item_config_infos(db: Session, item_config: ItemConfig, image_size: Union[int, None] = None):
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

    item_config_info = ItemConfigurationInfo(
        brand_name=str(brand.brand_name),
        category_name=str(category.category_name),
        item_class_name=str(item_class.name),
        item_class_description=str(item_class.description),
        product_number=str(item_class.product_number),
        item_config_description=item_config_description,
        image_hash=str(item_config.image_hash),
        image_size=image_size,
        properties_hash=str(item_config.properties_hash),
    )
    return item_config_info
