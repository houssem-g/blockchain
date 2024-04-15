import csv
import io
from typing import Dict, List

import fastapi
from app.api.utils.base.brand import get_brand_from_name
from app.api.utils.base.item_class import get_item_class_from_product_number
from app.api.utils.base.item_configuration import (
    create_item_configuration, delete_item_config,
    get_item_config_by_description_json)
from app.api.utils.base.role import BRAND_ROLE_NAMES_DICT
from app.api.utils.base.user_has_role import check_user_has_role_for_brand
from app.api.utils.base.user_profile import get_current_user_profile
from app.api.utils.item_config_utils import get_item_config_infos
from app.core.schemas.item_configuration import (ItemConfiguration,
                                                 ItemConfigurationDeletion,
                                                 ItemConfigurationInfo)
from app.db.base import get_db
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.post(
    "/v1/items_configs", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=ItemConfigurationInfo
    )
async def create_item_configuration_route(
    product_number: str = Form(...),
    description_json: object = Form(...),
    image: UploadFile = File(...),
    brand_name: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to create item configs.."
        )

    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist.."
        )

    item_class = await get_item_class_from_product_number(db, product_number, int(str(brand.brand_id)))

    if item_class is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"item class with product number {product_number} does not exist.."
        )

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], str(brand.brand_name)
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {str(brand.brand_name)}"
            )

    item_conf = ItemConfiguration(
        product_number=product_number, description_json=description_json, brand_name=brand_name
        )

    image_binary = await image.read()

    if not isinstance(image_binary, bytes):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"image file could not be read as binary: {image_binary}",
        )

    new_item_conf, image_size = await create_item_configuration(db=db, item_conf=item_conf, image_binary=image_binary)
    new_item_conf_infos = await get_item_config_infos(db, new_item_conf, image_size)
    return new_item_conf_infos


@router.post(
    "/v1/items_configs/list",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=List[ItemConfigurationInfo],
    )
async def create_item_configurations_list_route(
    item_configs_csv: UploadFile = File(...),
    images: List[UploadFile] = File(..., description="Multiple files as UploadFile"),
    brand_name: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    # TODO: add access control for the brand admin..
    if current_user_profile.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to create item configs.."
        )

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {brand_name}"
            )

    csv_binary = await item_configs_csv.read()
    if not isinstance(csv_binary, bytes):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"item configs csv file could not be read as binary: {csv_binary}",
        )

    list_of_configs_dict: List[Dict[str, str]] = list(csv.DictReader(io.StringIO(csv_binary.decode('utf-8'))))

    dict_of_images = {image.filename: image for image in images}

    list_of_configs = [
        (cfg.pop("product_number"), dict_of_images[cfg.pop("image")], cfg) for cfg in list_of_configs_dict
    ]

    images_binaries: Dict[str, bytes] = {}

    all_created_item_conf_infos = []
    for (product_number, image, description_json) in list_of_configs:
        image_binary = images_binaries.get(image.filename, await image.read())
        if not isinstance(image_binary, bytes):
            raise HTTPException(
                status_code=HTTP_200_OK,
                detail=f"image file could not be read as binary: {image_binary}",
            )
        images_binaries[image.filename] = image_binary
        item_conf = ItemConfiguration(
            product_number=product_number, description_json=description_json, brand_name=brand_name
            )
        new_item_conf, image_size = await create_item_configuration(
            db=db, item_conf=item_conf, image_binary=image_binary
            )
        new_item_conf_infos = await get_item_config_infos(db, new_item_conf, image_size)
        all_created_item_conf_infos.append(new_item_conf_infos)

    return all_created_item_conf_infos


@router.delete(
    "/v1/items_configs/delete",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ItemConfigurationDeletion,
    )
async def delete_item_config_route(
    db: Session = fastapi.Depends(get_db),
    product_number: str = Form(...),
    description_json: object = Form(...),
    brand_name: str = Form(...),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to delete item classes.."
        )

    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist.."
        )

    item_class = await get_item_class_from_product_number(db, product_number, int(str(brand.brand_id)))

    if item_class is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"the item class with PN {product_number} does not exist.."
            )

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], str(brand.brand_name)
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {brand.brand_name}"
            )

    to_delete = await delete_item_config(db, product_number, description_json, brand_name)
    return to_delete


@router.get(
    "/v1/items_configs", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=ItemConfigurationInfo
    )
async def get_items_configs_from_pn_route(
    db: Session = fastapi.Depends(get_db),
    product_number: str = Form(...),
    description_json: object = Form(...),
    brand_name: str = Form(...),
):

    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist..."
        )

    item_class = await get_item_class_from_product_number(db, product_number, int(str(brand.brand_id)))
    if item_class is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"no item class exist with product number {product_number}.."
        )

    item_config = await get_item_config_by_description_json(
        db=db, item_class_id=int(str(item_class.item_class_id)), description_json=description_json
    )
    if item_config is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"item config with product number {product_number} does not exist.."
        )
    item_config_infos = await get_item_config_infos(db, item_config)
    return item_config_infos


@router.post("/v1/upload")
async def upload(files: UploadFile = File(...)):
    await files.read()
    return files.filename
