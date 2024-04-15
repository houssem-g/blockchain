
import hashlib
from datetime import datetime
from random import randbytes
from typing import Tuple, Union

from app.core.emails import Email
from app.core.hashing import AuthService, oauth2_scheme
from app.core.schemas.token import TokenData
from app.core.schemas.user_profile import UserProfileCreate, UserTypes
from app.db.base import get_db
from app.db.models.email_confirmation import EmailConfirmation
from app.db.models.user_profile import UserProfile
from app.db.settings import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt  # type: ignore
from pydantic import EmailStr
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

EMAIL_CONFIRMATION_MAX_DURATION_MINUTES = 15


async def get_user_by_email(db: Session, email: str):
    user_recorded = db.query(UserProfile).filter(UserProfile.email == email).first()
    return user_recorded


async def get_user_profile_by_user_profile_id(db: Session, user_profile_id: int):
    user_profile_recorded = db.query(UserProfile).filter(UserProfile.user_profile_id == user_profile_id).first()
    return user_profile_recorded


async def get_user_profile_id_by_email(db: Session, email: str) -> int:
    user_profile_id: Union[Tuple[int], None] = db.query(
        UserProfile.user_profile_id
    ).filter(UserProfile.email == email).first()
    if user_profile_id is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"UserProfile with email {email} is not registered..",
        )
    return user_profile_id[0]


async def get_user_profile_by_username(db: Session, username: str) -> Union[UserProfile, None]:
    user_profile = db.query(UserProfile).filter(
        UserProfile.username == username and UserProfile.is_active is True
    ).first()
    return user_profile


async def check_if_email_confirmation_is_expired(email_confirmation: EmailConfirmation):
    now = datetime.strptime(str(datetime.utcnow()), "%Y-%m-%d %H:%M:%S.%f")
    last_email_confirmation_request_time = datetime.strptime(
        str(email_confirmation.updated_at), "%Y-%m-%d %H:%M:%S.%f"
    )
    diff = (now - last_email_confirmation_request_time).total_seconds() / 60.0
    if (diff > EMAIL_CONFIRMATION_MAX_DURATION_MINUTES):
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="Your confirmation link expired, please request a new email for confirmation!"
            )


async def confirm_email_with_code(db: Session, confirmation_code: str):
    hashed_code = hashlib.sha256()
    hashed_code.update(bytes.fromhex(confirmation_code))
    confirmation_code = hashed_code.hexdigest()

    code_confirmation_query_results = db.query(EmailConfirmation).filter(EmailConfirmation.code == confirmation_code)
    email_confirmation: Union[None, EmailConfirmation] = code_confirmation_query_results.first()

    if email_confirmation is None:
        raise HTTPException(status_code=HTTP_200_OK, detail="This confirmation code is wrong !")

    elif (email_confirmation.status == "confirmed"):
        raise HTTPException(status_code=HTTP_200_OK, detail="Email Already Confirmed, please login.")

    await check_if_email_confirmation_is_expired(email_confirmation)
    confirmed_email = email_confirmation.email
    code_confirmation_query_results.update({
        "status": "confirmed",
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        })
    db.commit()
    db.close()

    get_user_profile = db.query(UserProfile).filter(UserProfile.email == confirmed_email)
    get_user_profile.update({"is_active": True})
    db.commit()
    db.close()

    return "UserProfile activated !"


async def check_if_email_confirmed(db: Session, email: str):
    email_confirmation = db.query(EmailConfirmation).filter(EmailConfirmation.email == email).first()
    if email_confirmation is not None:
        await check_if_email_confirmation_is_expired(email_confirmation)
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="A confimation link has been sent to your email, please check your email and spam."
            )
    else:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="cannot find this email in email confirmation, please use a new email or contact our support!"
            )


async def check_if_username_is_used(db: Session, email: str, username: str):
    user_email_already_recorded = db.query(UserProfile).filter(
        UserProfile.email == email and UserProfile.is_active is True
    ).first()
    username_already_recorded = db.query(UserProfile).filter(
        UserProfile.username == username and UserProfile.is_active is True
    ).first()
    if user_email_already_recorded is not None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="This email is already used. Please login or register with another email."
            )
    elif username_already_recorded is not None and user_email_already_recorded is None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail="That username is already taken. Please try another one."
            )
    else:
        return None


async def add_new_user_to_db(
    db: Session, user_create: UserProfileCreate, on_admin_flag: bool, require_email_confirmation: bool
):
    user_to_update_results = db.query(UserProfile).filter(
        UserProfile.email == user_create.email and UserProfile.is_active is False
    )
    user_to_update: Union[UserProfile, None] = user_to_update_results.first()

    if user_to_update is not None:
        user_to_update_results.update({"updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")})
        db.commit()

    else:
        get_password_and_salt = AuthService.create_salt_and_hashed_password(plaintext_password=user_create.password)
        user_to_update = UserProfile(
            email=user_create.email,
            username=user_create.username,
            hashed_password=get_password_and_salt.password,
            salt=get_password_and_salt.salt,
            user_type=UserTypes.ON_ADMIN if on_admin_flag else UserTypes.SIMPLE_USER,
            is_active=False if require_email_confirmation else True,
        )
        db.add(user_to_update)
        db.commit()
        db.refresh(user_to_update)

    db.close()

    return user_to_update


async def add_new_email_confirmation_to_db(
    db: Session, user_create: UserProfileCreate, confirmation_code: str, confirmation_token: bytes
):

    email_confirmation_query_results = db.query(EmailConfirmation).filter(
        EmailConfirmation.email == user_create.email and
        EmailConfirmation.status == "not_confirmed"
        )
    email_confirmation: Union[None, EmailConfirmation] = email_confirmation_query_results.first()

    try:
        await Email(str(user_create.username), confirmation_token, [EmailStr(user_create.email)]).sendMail()
    except Exception as error:
        await delete_user_profile(db, user_create.username)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'There was an error sending email: {error}')

    if email_confirmation is None:

        email_confirmation = EmailConfirmation(
            email=user_create.email,
            code=confirmation_code,
            status="not_confirmed",
        )

        db.add(email_confirmation)
        db.commit()
        db.refresh(email_confirmation)

    else:
        email_confirmation_query_results.update({
            "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "code": confirmation_code,
            })
        db.commit()

    db.close()


async def create_new_user_profile(
    db: Session, user_profile_create: UserProfileCreate, on_admin_flag=False, require_email_confirmation=True
):
    await check_if_username_is_used(db, user_profile_create.email, user_profile_create.username)

    confirmation_token = randbytes(10)
    hashed_code = hashlib.sha256()
    hashed_code.update(confirmation_token)
    confirmation_code = hashed_code.hexdigest()

    if(settings.db_name == "test"):
        confirmation_token = b'\xb9'
        hashed_code = hashlib.sha256()
        hashed_code.update(confirmation_token)
        confirmation_code = hashed_code.hexdigest()

    new_user = await add_new_user_to_db(db, user_profile_create, on_admin_flag, require_email_confirmation)
    if require_email_confirmation:
        await add_new_email_confirmation_to_db(db, user_profile_create, confirmation_code, confirmation_token)
    return new_user


async def delete_user_profile(db: Session, username: str):

    user_profile = await get_user_profile_by_username(db, username)
    # if user_profile with given id exists, delete it from the database. Otherwise raise 404 error
    if user_profile:
        db.delete(user_profile)
        db.commit()
        db.close()
    else:
        raise HTTPException(status_code=404, detail=f"user_profile with username {username} not found")
    return "user_profile is deleted!"


async def create_jw_token(db, form_data: OAuth2PasswordRequestForm):

    user_profile: Union[UserProfile, None] = AuthService.authenticate(
        email=form_data.username, password=form_data.password, db=db
    )
    if user_profile is None:
        raise HTTPException(status_code=200, detail="Incorrect username or password")

    if settings.db_name != "test" and user_profile.is_active is False:
        await check_if_email_confirmed(db, form_data.username)

    return {
        "access_token": AuthService.create_access_token(sub=str(user_profile.user_profile_id)),
        "token_type": "bearer",
    }


async def get_current_user_profile(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserProfile:
    # skipping for simplicity...
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.algorithm],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")  # type: ignore
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_profile = db.query(UserProfile).filter(UserProfile.user_profile_id == token_data.username).first()
    if user_profile is None:
        raise credentials_exception
    return user_profile


async def update_user_profile_username(db: Session, username: str, new_username: str):
    if await get_user_profile_by_username(db, new_username) is not None:
        raise HTTPException(status_code=HTTP_200_OK, detail="That username is already taken. Please try another one.")

    get_user_profile = db.query(UserProfile).filter(UserProfile.username == username)
    get_user_profile.update({"username": new_username})
    db.commit()
    db.close()
    return "UserProfile updated with success !"


async def update_user_profile_description(db: Session, username: str, description: str):
    get_user_profile = db.query(UserProfile).filter(UserProfile.username == username)
    get_user_profile.update({"description": description})
    db.commit()
    db.close()
    return "UserProfile updated with success !"
