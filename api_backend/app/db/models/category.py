from app.db.base import Base
from sqlalchemy import Column, Integer, String  # type: ignore

from .mixins import Timestamp


class Category(Timestamp, Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False, unique=True)
