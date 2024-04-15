from app.db.base import Base
from sqlalchemy import Column, Integer, String  # type: ignore

from .mixins import Timestamp


class Role(Timestamp, Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False)
