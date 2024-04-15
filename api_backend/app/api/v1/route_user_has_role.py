
from typing import List, Tuple

import fastapi
from app.api.utils.base.brand import get_brand_from_id, get_brand_from_name
from app.api.utils.base.role import (BRAND_ROLE_NAMES_DICT, get_role_by_id,
                                     get_role_by_name)
from app.api.utils.base.user_has_role import (check_user_has_role_for_brand,
                                              get_user_has_roles_of_a_brand,
                                              get_user_has_role_list_of_username)
from app.api.utils.base.user_profile import (
    get_current_user_profile, get_user_profile_by_user_profile_id)
from app.core.schemas.user_profile import UserTypes
from app.db.base import get_db
from app.db.models.brand import Brand
from app.db.models.role import Role
from app.db.models.user_profile import UserProfile
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.get(
    "/v1/roles/brand/{brand_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
)
async def get_all_users_with_any_role_for_a_brand_route(
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user.user_type in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        if current_user.user_type == UserTypes.BUSINESS_ADMIN:
            current_username = str(current_user.username)
            roles_of_current_user = await get_user_has_role_list_of_username(db, current_username)

            brand = await get_brand_from_name(db=db, brand_name=brand_name)
            if brand is None:
                raise HTTPException(
                    status_code=HTTP_200_OK,
                    detail=f"The brand {brand_name} does not exist..",
                )

            if brand.brand_id not in [role.brand_id for role in roles_of_current_user]:
                raise HTTPException(
                    status_code=HTTP_200_OK,
                    detail=f"you are not admin of the brand {brand_name}",
                )

        user_has_roles = await get_user_has_roles_of_a_brand(db, brand_name)

        response = [
            {
                "username": await get_user_profile_by_user_profile_id(db, int(str(user_has_role_iter.user_profile_id))),
                "brand_name": brand_name,
                "role_name": await get_role_by_id(db, int(str(user_has_role_iter.role_id))),
            }
            for user_has_role_iter in user_has_roles
        ]

        response = [
            {
                "username": response_iter["username"].username,
                "brand_name": response_iter["brand_name"],
                "role_name": response_iter["role_name"].role_name,
            }
            for response_iter in response
        ]

        return response

    raise HTTPException(
            status_code=HTTP_200_OK, detail="only brand admins and ON-Limited admins can access this route"
        )


@router.get(
    "/v1/roles/user/{username}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
)
async def get_roles_from_username_route(
    username: str,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    user_has_roles = []
    if current_user.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        if username != current_user.username:
            raise HTTPException(
                status_code=HTTP_200_OK, detail="you cannot access the roles of someone else.."
            )
        user_has_roles = await get_user_has_role_list_of_username(db, username)

    if current_user.user_type == UserTypes.BUSINESS_ADMIN:
        user_has_roles_of_current_user = await get_user_has_role_list_of_username(db, str(current_user.username))
        business_admin_role = await get_role_by_name(db, BRAND_ROLE_NAMES_DICT["business_admin"])
        if business_admin_role is None:
            raise HTTPException(
                status_code=HTTP_200_OK, detail="no role created for business admin.."
            )
        brand_ids_current_user_is_admin_of = [
            user_has_role.brand_id
            for user_has_role in user_has_roles_of_current_user
            if user_has_role.role_id == business_admin_role.role_id
        ]
        user_has_roles = await get_user_has_role_list_of_username(db, username)
        user_has_roles = [
            user_has_role
            for user_has_role in user_has_roles
            if user_has_role.brand_id in brand_ids_current_user_is_admin_of
        ]

    if current_user.user_type == UserTypes.ON_ADMIN:
        user_has_roles = await get_user_has_role_list_of_username(db, username)

    list_of_username_brand_role: List[Tuple[str, Brand, Role]] = []
    for user_has_role in user_has_roles:
        brand = await get_brand_from_id(db, int(str(user_has_role.brand_id)))
        role = await get_role_by_id(db, int(str(user_has_role.role_id)))

        if brand is None or role is None:
            raise HTTPException(
                status_code=HTTP_200_OK, detail="brand or role does not exist.."
            )
        list_of_username_brand_role.append((username, brand, role))

    response = [
        {
            "username": username,
            "brand_name": brand.brand_name,
            "role_name": role.role_name,
        }
        for username, brand, role in list_of_username_brand_role
    ]

    return response


@router.get(
    "/v1/roles/users/{username}/is_business_admin/{brand_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
)
async def is_this_user_admin_of_this_brand_route(
    username: str,
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user: UserProfile = fastapi.Depends(get_current_user_profile)
):
    return await check_user_has_role_for_brand(
            db, str(current_user.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )
