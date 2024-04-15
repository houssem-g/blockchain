from app.db.base import Base
from sqlalchemy import (Column, ForeignKey, Integer, String,  # type: ignore
                        UniqueConstraint)
from sqlalchemy.orm import relationship  # type: ignore

from .mixins import Timestamp


class ItemClass(Timestamp, Base):
    __tablename__ = "item_class"

    item_class_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    product_number = Column(String(100))
    description = Column(String(256))
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brand.brand_id"), nullable=False)

    category = relationship("Category", backref="item_class")
    brand = relationship("Brand", backref="item_class")
    __table_args__ = (UniqueConstraint('brand_id', 'product_number', name='_brand_pn_uc'),)
