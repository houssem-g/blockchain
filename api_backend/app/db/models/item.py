from app.core.schemas.item import ItemStatus
from app.db.base import Base
from sqlalchemy import (Column, Enum, ForeignKey, Integer,  # type: ignore
                        String)
from sqlalchemy.orm import relationship  # type: ignore

from .mixins import Timestamp


class Item(Timestamp, Base):
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(ItemStatus))
    user_profile_id = Column(Integer, ForeignKey("user_profile.user_profile_id"), nullable=True)
    item_configuration_id = Column(Integer, ForeignKey("item_configuration.item_config_id"), nullable=False)
    serial_number = Column(String(100))
    activation_key = Column(String(10), unique=True,)
    parent_user_profile = relationship("UserProfile", backref="item")
    parent_item_conf = relationship("ItemConfig", backref="item")
