from app.db.base import Base
from app.db.models.mixins import Timestamp
from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy_utils import URLType  # type: ignore


class Brand(Timestamp, Base):
    __tablename__ = "brand"

    brand_id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(100), nullable=False, unique=True)
    logo_url = Column(URLType)
    website = Column(URLType)
    description = Column(String(150))
