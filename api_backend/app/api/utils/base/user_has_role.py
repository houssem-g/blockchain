from typing import List, Union

from app.api.utils.base.brand import get_brand_from_name
from app.api.utils.base.role import BRAND_ROLE_NAMES_DICT, get_role_by_name
from app.api.utils.base.user_profile import get_user_profile_by_username
from app.core.schemas.user_profile import UserTypes
from app.db.models.user_has_role import UserHasRole
from app.db.models.user_profile import UserProfile
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_user_has_roles_of_a_brand(db: Session, brand_name: str) -> List[UserHasRole]:
    brand = await get_brand_from_name(db=db, brand_name=brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The brand {brand_name} does not exist..",
        )
    users_has_roles: List[UserHasRole] = (
        db.query(UserHasRole).filter(UserHasRole.brand_id == brand.brand_id).limit(1000).all()
    )
    if len(users_has_roles) == 0:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The brand {brand_name} does not have any users..",
        )
    return users_has_roles


async def check_user_has_role_for_brand(db: Session, username: str, role_name: str, brand_name: str):
    user_profile = await get_user_profile_by_username(db=db, username=username)
    if user_profile is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The user_profile with username {username} does not exist..",
        )

    role = await get_role_by_name(db=db, role_name=role_name)
    if role is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The role {role_name} does not exist..",
        )

    brand = await get_brand_from_name(db=db, brand_name=brand_name)
    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The brand {brand_name} does not exist..",
        )

    is_user: Union[None, List[UserHasRole]] = db.query(UserHasRole).filter(
        UserHasRole.user_profile_id == user_profile.user_profile_id
    ).filter(
        UserHasRole.role_id == role.role_id
    ).filter(
        UserHasRole.brand_id == brand.brand_id
    ).first()

    return bool(is_user)


async def get_user_has_role_list_of_username(db: Session, username: str) -> List[UserHasRole]:
    user_profile = await get_user_profile_by_username(db=db, username=username)
    if user_profile is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The user_profile with username {username} does not exist..",
        )
    user_has_role_list: List[UserHasRole] = db.query(UserHasRole).filter(
        UserHasRole.user_profile_id == user_profile.user_profile_id
    ).limit(1000).all()
    if len(user_has_role_list) == 0:
        user_has_role_list = []
    return user_has_role_list


async def make_business_admin(username: str, brand_name: str, db: Session, current_user_profile: UserProfile):
    if current_user_profile.user_type != UserTypes.ON_ADMIN:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="Only ON-Limited Admins can create new Business Admins",
        )
    user_to_change_status = await get_user_profile_by_username(db=db, username=username)
    if user_to_change_status is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The user_profile with username {username} does not exist..",
        )
    user_type = UserTypes.BUSINESS_ADMIN

    brand = await get_brand_from_name(db, brand_name)

    if not brand:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"brand {brand_name} does not exist..",
        )

    business_admin_role = await get_role_by_name(db, BRAND_ROLE_NAMES_DICT["business_admin"])

    if business_admin_role is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"Business admin role {BRAND_ROLE_NAMES_DICT['business_admin']} is not created..",
        )

    user_has_role = UserHasRole(
        brand_id=brand.brand_id,
        role_id=business_admin_role.role_id,
        user_profile_id=user_to_change_status.user_profile_id
    )

    setattr(user_to_change_status, "user_type", user_type)

    db.add(user_to_change_status)
    db.commit()
    db.refresh(user_to_change_status)

    db.add(user_has_role)
    db.commit()
    db.refresh(user_has_role)

    updated_user_profile = await get_user_profile_by_username(db=db, username=username)
    if updated_user_profile is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The user_profile with username {username} does not exist..",
        )

    updated_user_has_role_list_of_username = await get_user_has_role_list_of_username(db, username)
    assert updated_user_profile.user_type == user_type, f"user_profile {updated_user_profile} failed to become admin.."
    assert any([
        user_has_role_iter.brand_id == brand.brand_id and
        user_has_role_iter.role_id == business_admin_role.role_id and
        user_has_role_iter.user_profile_id == updated_user_profile.user_profile_id
        for user_has_role_iter in updated_user_has_role_list_of_username
    ])

    return {"username": username, "role_name": business_admin_role.role_name, "brand_name": brand.brand_name}


async def revoke_business_admin(username: str, brand_name: str, db: Session, current_user_profile: UserProfile):
    if current_user_profile.user_type not in [UserTypes.ON_ADMIN, UserTypes.BUSINESS_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="Only ON-Limited Admins or the brand admins can revoke Business Admin rights",
        )

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        business_admin_role = await get_role_by_name(db, BRAND_ROLE_NAMES_DICT["business_admin"])
        if business_admin_role is None:
            raise HTTPException(
                status_code=HTTP_200_OK,
                detail=f"Business admin role {BRAND_ROLE_NAMES_DICT['business_admin']} is not created..",
            )

        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK,
                detail="Only ON-Limited Admins or the brand admins can revoke Business Admin rights",
            )

    user_profile_to_change_status = await get_user_profile_by_username(db=db, username=username)

    brand = await get_brand_from_name(db, brand_name)

    if brand is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"brand {brand_name} does not exist..",
        )

    user_has_role_list_of_username = await get_user_has_role_list_of_username(db, username)

    for user_has_role in user_has_role_list_of_username:
        if user_has_role.brand_id == brand.brand_id:
            db.delete(user_has_role)
            db.commit()
            db.close()

    new_user_has_roles_of_user = await get_user_has_role_list_of_username(db, username)

    if len(new_user_has_roles_of_user) == 0:
        user_type = UserTypes.SIMPLE_USER
        setattr(user_profile_to_change_status, "user_type", user_type)
        db.add(user_profile_to_change_status)
        db.commit()
        db.refresh(user_profile_to_change_status)

    assert not any([
        user_has_role for user_has_role in new_user_has_roles_of_user if user_has_role.brand_id == brand.brand_id
    ]), f"user_profile with username {username} still has roles for the brand {brand_name}"

    return user_profile_to_change_status
