import csv
import io
from typing import Dict, List

import fastapi
from app.api.utils.base.brand import get_brand_from_id
from app.api.utils.base.item_class import (delete_item_class,
                                           get_item_class_by_name)
from app.api.utils.base.role import BRAND_ROLE_NAMES_DICT
from app.api.utils.base.user_has_role import check_user_has_role_for_brand
from app.api.utils.base.user_profile import get_current_user_profile
from app.api.utils.item_class_utils import (create_item_class,
                                            get_item_class_infos)
from app.core.schemas.item_class import (ItemClassDeletion, ItemClassInfo,
                                         ItemClassInput)
from app.db.base import get_db
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import File, HTTPException, UploadFile
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


# TODO:
# - prevent deletion if any item of the item class is already distributed and active
# - if we delete an item class, it should delete all of its configs and items..

@router.post(
    "/v1/items_classes", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=ItemClassInfo
)
async def create_item_class_route(
    item_class: ItemClassInput,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(status_code=HTTP_200_OK, detail="you do not have the right to create item classes..")

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], item_class.brand_name
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {item_class.brand_name}"
            )

    new_item_class = await create_item_class(db=db, item_class=item_class)
    new_item_class_info = await get_item_class_infos(db, new_item_class)
    return new_item_class_info


@router.post(
    "/v1/items_classes/list",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=List[ItemClassInfo]
)
async def create_item_classes_list_route(
    item_classes_csv: UploadFile = File(...),
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to create item classes.."
        )

    csv_binary = await item_classes_csv.read()
    if not isinstance(csv_binary, bytes):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"item classes csv file could not be read as binary: {csv_binary}",
        )

    list_of_item_classes_dict: List[Dict[str, str]] = list(csv.DictReader(io.StringIO(csv_binary.decode('utf-8'))))
    new_item_classes_info = []

    for item_class_dict in list_of_item_classes_dict:
        item_class = ItemClassInput(**item_class_dict)
        if current_user.user_type == UserTypes.BUSINESS_ADMIN:
            current_user_is_brand_admin = await check_user_has_role_for_brand(
                db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], item_class.brand_name
            )
            if not current_user_is_brand_admin:
                raise HTTPException(
                    status_code=HTTP_200_OK, detail=f"you are not admin of the brand {item_class.brand_name}"
                )

        new_item_class = await create_item_class(db=db, item_class=item_class)
        new_item_class_info = await get_item_class_infos(db, new_item_class)
        new_item_classes_info.append(new_item_class_info)

    return new_item_classes_info


@router.delete(
    "/v1/items_classes/delete/{item_class_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ItemClassDeletion,
)
async def delete_item_class_route(
    item_class_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to delete item classes.."
        )

    item_class = await get_item_class_by_name(db, item_class_name)

    if item_class is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"the item class {item_class_name} does not exist.."
            )

    brand = await get_brand_from_id(db, int(str(item_class.brand_id)))
    if brand is None:
        raise HTTPException(
                status_code=HTTP_200_OK, detail=f"the brand {item_class.brand_id} does not exist.."
            )

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], str(brand.brand_name)
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {brand.brand_name}"
            )

    to_delete = await delete_item_class(db=db, item_class_name=item_class_name)
    return to_delete
