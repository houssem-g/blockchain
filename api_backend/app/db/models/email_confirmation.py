from app.db.base import Base
from sqlalchemy import Column, String  # type: ignore

from .mixins import Timestamp


class EmailConfirmation(Timestamp, Base):
    __tablename__ = "email_confirmation"

    email = Column(String(100), primary_key=True, index=True)
    status = Column(String(100), nullable="not_confirmed")
    code = Column(String(100), nullable=False)
