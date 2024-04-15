from app.core.schemas.user_profile import UserTypes
from app.db.base import Base
from sqlalchemy import Boolean, Column, Enum, Integer, String  # type: ignore
from sqlalchemy_utils import URLType  # type: ignore

from .mixins import Timestamp


class UserProfile(Timestamp, Base):
    __tablename__ = "user_profile"

    user_profile_id = Column(Integer, primary_key=True, index=True)
    user_type = Column(Enum(UserTypes), default=UserTypes.SIMPLE_USER)

    first_name = Column(String(256), default="")
    last_name = Column(String(256), default="")

    username = Column(String(256), nullable=False, unique=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    salt = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=False)

    address = Column(String(256), default="")
    phone_number = Column(String(256), default="")

    profile_picture_url = Column(URLType, default="")
    coverage_picture_url = Column(URLType, default="")
    description = Column(String(256), default="")
