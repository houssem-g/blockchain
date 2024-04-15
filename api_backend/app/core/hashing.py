from datetime import datetime, timedelta
from typing import Union

import bcrypt
from app.core.schemas.user_profile import UserPasswordUpdate
from app.db.models.user_profile import UserProfile
from app.db.settings import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


class AuthService:
    @staticmethod
    def create_salt_and_hashed_password(plaintext_password: str) -> UserPasswordUpdate:
        salt = AuthService.generate_salt()
        hashed_password = AuthService.hash_password(password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    @staticmethod
    def verify_password(password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)

    @staticmethod
    def authenticate(email: str, password: str, db: Session):
        user_profile: Union[UserProfile, None] = db.query(UserProfile).filter(UserProfile.email == email).first()
        if not user_profile:
            return None
        if not AuthService.verify_password(password, str(user_profile.salt), str(user_profile.hashed_password)):
            return None
        return user_profile

    @staticmethod
    def create_access_token(sub: str) -> str:
        return AuthService._create_token(
            token_type="access_token",
            lifetime=timedelta(minutes=settings.access_token_expire_minutes),
            sub=sub,
        )

    @staticmethod
    def _create_token(token_type: str, lifetime: timedelta, sub: str):
        payload = {}
        expire = datetime.utcnow() + lifetime
        payload["type"] = token_type
        payload["exp"] = expire  # type: ignore
        payload["iat"] = datetime.utcnow()  # type: ignore
        payload["sub"] = str(sub)

        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.algorithm)
