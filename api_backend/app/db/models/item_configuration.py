from app.db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String  # type: ignore
from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .mixins import Timestamp


class ItemConfig(Timestamp, Base):
    __tablename__ = "item_configuration"

    item_config_id = Column(Integer, primary_key=True, index=True)
    item_class_id = Column(Integer, ForeignKey("item_class.item_class_id"), nullable=False)
    image_hash = Column(String(50))
    properties_hash = Column(String(50))
    description_json = Column(JSONB, nullable=False, server_default="{}")
    parent_item_class = relationship("ItemClass", backref="item_configuration")
