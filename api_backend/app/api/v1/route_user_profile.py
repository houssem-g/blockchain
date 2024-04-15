

import fastapi
from app.api.utils.base.user_has_role import (make_business_admin,
                                              revoke_business_admin)
from app.api.utils.base.user_profile import (confirm_email_with_code,
                                             create_jw_token,
                                             create_new_user_profile,
                                             delete_user_profile,
                                             get_current_user_profile,
                                             get_user_profile_by_username,
                                             update_user_profile_description,
                                             update_user_profile_username)
from app.core.schemas.token import Token
# from api.utils import users
from app.core.schemas.user_profile import (ShowUserProfile, UserProfileCreate,
                                           UserTypes)
from app.db.base import get_db
from app.db.models.user_profile import UserProfile
from app.db.settings import settings
from fastapi import Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.post("/v1/users/signup", response_model=ShowUserProfile)
async def create_user_route(user_profile_create: UserProfileCreate, db: Session = fastapi.Depends(get_db)):
    response = await create_new_user_profile(db=db, user_profile_create=user_profile_create)
    return response


@router.post("/v1/users/login", response_model=Token)
async def login_route(db: Session = fastapi.Depends(get_db), form_data: OAuth2PasswordRequestForm = fastapi.Depends()):
    """
    Get the JWT for a user_profile with data from OAuth2 request form body.
    """
    return await create_jw_token(db, form_data)


@router.post(
    "/v1/users/{username}/make_business_admin/{brand_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)]
)
async def make_business_admin_route(
    username: str,
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    return await make_business_admin(
        username=username, db=db, brand_name=brand_name, current_user_profile=current_user_profile
    )


@router.delete(
    "/v1/users/{username}/revoke_business_admin/{brand_name}",
    dependencies=[fastapi.Depends(get_current_user_profile)],
    response_model=ShowUserProfile
)
async def revoke_business_admin_route(
    username: str,
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    return await revoke_business_admin(
        username=username, db=db, brand_name=brand_name, current_user_profile=current_user_profile
    )


@router.get("/v1/users/me", response_model=ShowUserProfile)
async def user_me_route(current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)):
    """
    Fetch the current logged in user_profile.
    """
    return current_user_profile


@router.delete("/v1/users/delete/{username}", dependencies=[fastapi.Depends(get_current_user_profile)])
async def delete_user_route(
    username: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile)
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN or current_user_profile.username == username:
        toDel = await delete_user_profile(db, username)
        return toDel
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"you do not have the right to delete {username}")


@router.post(
    "/v1/users/{username}", dependencies=[fastapi.Depends(get_current_user_profile)], response_model=ShowUserProfile
)
async def get_user_from_username_route(
    username: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile),
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN or current_user_profile.username == username:
        user_profile = await get_user_profile_by_username(db=db, username=username)
        return user_profile
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"you do not have the right to get the username {username}")


@router.put("/v1/users/username_update", dependencies=[fastapi.Depends(get_current_user_profile)])
async def update_username_route(
    username: str = Form(...),
    new_username: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile),
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN or current_user_profile.username == username:
        response = await update_user_profile_username(db=db, username=username, new_username=new_username)
        return response
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"you do not have the right to get the username {username}")


@router.put("/v1/users/description_update", dependencies=[fastapi.Depends(get_current_user_profile)])
async def update_description_route(
    username: str = Form(...),
    description: str = Form(...),
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile),
):
    if current_user_profile.user_type == UserTypes.ON_ADMIN or current_user_profile.username == username:
        response = await update_user_profile_description(db=db, username=username, description=description)
        return response
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"you do not have the right to get the username {username}")


@router.get("/v1/users/confirm_email/{confirmation_code}")
async def confirm_email_with_code_route(confirmation_code: str, db: Session = fastapi.Depends(get_db)):
    await confirm_email_with_code(db=db, confirmation_code=confirmation_code)
    url_redirection = f"{settings.frontend_URI}/user-profil-confirmed"
    return RedirectResponse(url_redirection)
