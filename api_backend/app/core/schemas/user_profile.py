from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserTypes(str, Enum):
    SIMPLE_USER = "simple_user"
    BUSINESS_USER = "business_user"
    BUSINESS_ADMIN = "business_admin"
    ON_ADMIN = "on_admin"


class UserProfileBase(BaseModel):
    email: str


class UserProfileCreate(UserProfileBase):
    """
    class needed during user_profile creation
    """

    username: str
    email: EmailStr
    password: str


class UserProfile(UserProfileBase):

    user_profile_id: int
    is_active: bool

    create_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ShowUserProfile(UserProfileBase):
    username: str
    email: EmailStr
    user_type: str

    class Config:
        orm_mode = True


class UserPasswordUpdate(BaseModel):
    """
    Users can change their password
    """
    password: str
    salt: str
