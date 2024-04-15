import csv
import io
from typing import Dict, List

import fastapi
import requests
from app.api.utils.base.brand import get_brand_from_name
from app.api.utils.base.item import (activate_item, burn_item, create_item,
                                     delete_item, get_item_by_serial_number,
                                     get_items_of_username,
                                     transfer_item_to_username)
from app.api.utils.base.role import BRAND_ROLE_NAMES_DICT
from app.api.utils.base.user_has_role import check_user_has_role_for_brand
from app.api.utils.base.user_profile import get_current_user_profile
from app.api.utils.item_utils import (
    get_item_infos, get_items_from_brand_name, get_items_infos,
    get_qr_codes_from_items_infos_in_a_zip_file)
from app.core.schemas.item import (ItemCreation, ItemDeletion, ItemInfo,
                                   ItemTransfered)
from app.core.web3_utils.ipfs import get_ipfs_config
from app.db.base import get_db
from app.db.models.item import ItemStatus
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore
from starlette.responses import StreamingResponse
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.post("/v1/items/create", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=ItemInfo)
async def create_item_route(
    serial_number: str = Form(...),
    product_number: str = Form(...),
    config_decription_json: object = Form(...),
    brand_name: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to create items.."
        )

    brand = await get_brand_from_name(db, brand_name)

    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist.."
        )

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], str(brand.brand_name)
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {str(brand.brand_name)}"
            )

    item = ItemCreation(
        serial_number=serial_number, product_number=product_number, config_decription_json=config_decription_json
    )

    new_item = await create_item(db, item, int(str(brand.brand_id)))
    new_item_infos = await get_item_infos(db, new_item)
    return new_item_infos


@router.post(
    "/v1/items/create/list", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=List[ItemInfo]
    )
async def create_items_list_route(
    items_csv: UploadFile = File(...),
    db: Session = fastapi.Depends(get_db),
    brand_name: str = Form(...),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to create items.."
        )

    brand = await get_brand_from_name(db, brand_name)

    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist.."
        )

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], str(brand.brand_name)
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {str(brand.brand_name)}"
            )

    csv_binary = await items_csv.read()
    if not isinstance(csv_binary, bytes):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"item configs csv file could not be read as binary: {csv_binary}",
        )

    list_of_items_dict: List[Dict[str, str]] = list(csv.DictReader(io.StringIO(csv_binary.decode('utf-8'))))

    list_of_items = [
        (item.pop("serial_number"), item.pop("product_number"), item) for item in list_of_items_dict
    ]

    all_created_items_infos = []
    for serial_number, product_number, config_description_json in list_of_items:
        item = ItemCreation(
            serial_number=serial_number, product_number=product_number, config_decription_json=config_description_json
        )
        new_item = await create_item(db, item, int(str(brand.brand_id)))
        new_item_infos = await get_item_infos(db, new_item)
        all_created_items_infos.append(new_item_infos)

    return all_created_items_infos


@router.post(
    "/v1/items/transfer",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ItemTransfered,
)
async def transfer_item_route(
    brand_name: str = Form(...),
    serial_number: str = Form(...),
    username: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if username == current_user.username:
        raise HTTPException(
                status_code=HTTP_200_OK, detail="you cannot transfer an item to yourself.."
            )
    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"there is no brand {brand_name}.."
        )

    brand_id = int(str(brand.brand_id))
    item = await get_item_by_serial_number(db, serial_number, brand_id)

    if item is None:
        raise HTTPException(
                status_code=HTTP_200_OK,
                detail=f"you cannot transfer item with SN {serial_number} as you are not the owner"
            )

    if item.user_profile_id != current_user.user_profile_id:
        raise HTTPException(
                status_code=HTTP_200_OK,
                detail=f"you cannot transfer item with SN {serial_number} as you are not the owner"
            )

    item = await transfer_item_to_username(db=db, serial_number=serial_number, username=username, brand_id=brand_id)
    if item is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"you canno transfer item with SN {serial_number} to username {username}"
            )
    item_info = await get_item_infos(db, item)
    item_tranfered = ItemTransfered(
        brand_name=item_info.brand_name,
        category_name=item_info.category_name,
        item_class_name=item_info.item_class_name,
        item_class_description=item_info.item_class_description,
        product_number=item_info.product_number,
        item_config_description=item_info.item_class_description,
        activation_key=item_info.activation_key,
        image_hash_key=item_info.image_hash_key,
        serial_number=item_info.serial_number,
        status=item_info.status,
        transfered_to_username=username,
    )
    return item_tranfered


@router.post("/v1/items/activate", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=ItemInfo)
async def activate_item_route(
    activation_key: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):

    item = await activate_item(db, activation_key, int(str(current_user.user_profile_id)))
    item_infos = await get_item_infos(db, item)
    return item_infos


@router.post(
    "/v1/items/burn",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ItemDeletion,
)
async def burn_item_route(
    brand_name: str = Form(...),
    serial_number: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):

    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist.."
            )
    item = await get_item_by_serial_number(db, serial_number, int(str(brand.brand_id)))

    if item is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail="you cannot burn an item you do not own.."
            )

    if item.user_profile_id != current_user.user_profile_id:
        raise HTTPException(
                status_code=HTTP_200_OK, detail="you cannot burn an item you do not own.."
            )

    item = await burn_item(db, serial_number, int(str(brand.brand_id)))
    if item is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you cannot burn an item you do not own.."
        )
    item_info = await get_item_infos(db, item)
    return ItemDeletion(
        brand_name=item_info.brand_name,
        category_name=item_info.category_name,
        item_class_name=item_info.item_class_name,
        item_class_description=item_info.item_class_description,
        product_number=item_info.product_number,
        item_config_description=item_info.item_class_description,
        activation_key=item_info.activation_key,
        image_hash_key=item_info.image_hash_key,
        serial_number=item_info.serial_number,
        status=item_info.status,
        burn_status=True,
        delete_status=False,
    )


@router.get("/v1/imgs/{hash_key}")
async def get_img_from_path(hash_key: str):
    ipfs_config = get_ipfs_config()
    img_path = f"{ipfs_config.host_address}{hash_key}"
    image_data = requests.get(img_path).content
    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpg")


@router.delete(
    "/v1/items/delete/{brand_name}/{serial_number}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ItemDeletion,
)
async def delete_item_route(
    brand_name: str,
    serial_number: str,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to delete items.."
        )

    brand = await get_brand_from_name(db, brand_name)

    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"you cannot delete item with SN {serial_number} as its brand does not exist.."
        )

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], str(brand.brand_name)
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {brand.brand_name}"
            )

    item = await delete_item(db=db, serial_number=serial_number, brand_id=int(str(brand.brand_id)))
    item_info = await get_item_infos(db, item)
    return ItemDeletion(
        brand_name=item_info.brand_name,
        category_name=item_info.category_name,
        item_class_name=item_info.item_class_name,
        item_class_description=item_info.item_class_description,
        product_number=item_info.product_number,
        item_config_description=item_info.item_class_description,
        activation_key=item_info.activation_key,
        image_hash_key=item_info.image_hash_key,
        serial_number=item_info.serial_number,
        status=item_info.status,
        burn_status=False,
        delete_status=True,
    )


@router.get(
    "/v1/items/{brand_name}/{serial_number}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ItemInfo,
    )
async def get_item_route(serial_number: str, brand_name: str, db: Session = fastapi.Depends(get_db)):
    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"brand {brand_name} does not exist..."
        )

    item = await get_item_by_serial_number(db=db, serial_number=serial_number, brand_id=int(str(brand.brand_id)))
    if item is None:
        raise HTTPException(
            status_code=HTTP_200_OK, detail=f"item with serial number {serial_number} does not exist.."
        )
    item_infos = await get_item_infos(db, item)
    return item_infos


@router.get("/v1/users/{username}/items", dependencies=[fastapi.Depends(get_current_user_profile)])
async def get_items_from_username_route(
    username: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if username != current_user_profile.username and current_user_profile.user_type not in [UserTypes.ON_ADMIN]:
        raise HTTPException(
                status_code=HTTP_200_OK, detail="you cannot get an the items of another user_profile.."
            )

    items = await get_items_of_username(db=db, username=username)
    items_responses: List[ItemInfo] = await get_items_infos(db, items)
    return items_responses


# @router.get("/v1/get_qr_code/{activation_key}")
# async def get_qr_code(activation_key: str):
#     return await get_qr_codes_from_activation_keys_in_a_zip_file([activation_key])


@router.get(
    "/v1/brands/{brand_name}/items",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=List[ItemInfo]
)
async def get_items_from_brand_name_route(
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):

    has_access = False

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        has_access = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )

    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        has_access = True

    if not has_access:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to get the items of this brand.."
        )

    items = await get_items_from_brand_name(db, brand_name)

    all_items_info: List[ItemInfo] = await get_items_infos(db, items)
    return all_items_info


@router.get("/v1/brands/{brand_name}/items/qr_codes", dependencies=[fastapi.Depends(get_current_user_profile)])
async def get_items_qr_codes_from_brand_name_route(
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):

    has_access = False

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        has_access = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )

    if current_user_profile.user_type == UserTypes.ON_ADMIN:
        has_access = True

    if not has_access:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to get the items of this brand.."
        )

    items = await get_items_from_brand_name(db, brand_name)

    all_items_info: List[ItemInfo] = await get_items_infos(db, items)

    not_activated_items_info = [
        item_info for item_info in all_items_info if item_info.status == ItemStatus.NOT_ACTIVATED
    ]

    if len(not_activated_items_info) == 0:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="there are no items to get the qr codes from.."
        )

    return await get_qr_codes_from_items_infos_in_a_zip_file(not_activated_items_info)


@router.get(
    "/v1/brands/{brand_name}/items/{product_number}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=List[ItemInfo]
)
async def get_items_from_brand_name_with_PN_filter_route(
    brand_name: str,
    product_number: str,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):

    has_access = False

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        has_access = await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )

    if current_user.user_type == UserTypes.ON_ADMIN:
        has_access = True

    if not has_access:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to get the items of this brand.."
        )

    items = await get_items_from_brand_name(db, brand_name)

    all_items_info: List[ItemInfo] = await get_items_infos(db, items)

    all_items_info = [item_info for item_info in all_items_info if item_info.product_number == product_number]

    return all_items_info


@router.get(
    "/v1/brands/{brand_name}/items/{product_number}/qr_codes", dependencies=[fastapi.Depends(get_current_user_profile)]
)
async def get_items_qr_codes_from_brand_name_with_PN_filter_route(
    brand_name: str,
    product_number: str,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):

    has_access = False

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        has_access = await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )

    if current_user.user_type == UserTypes.ON_ADMIN:
        has_access = True

    if not has_access:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to get the items of this brand.."
        )

    items = await get_items_from_brand_name(db, brand_name)

    all_items_info: List[ItemInfo] = await get_items_infos(db, items)

    all_items_info = [item_info for item_info in all_items_info if item_info.product_number == product_number]

    not_activated_items_info = [
        item_info for item_info in all_items_info if item_info.status == ItemStatus.NOT_ACTIVATED
    ]

    if len(not_activated_items_info) == 0:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="there are no items to get the qr codes from.."
        )

    return await get_qr_codes_from_items_infos_in_a_zip_file(not_activated_items_info)
