from app.db.base import Base
from sqlalchemy import Column, ForeignKey, Integer  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .mixins import Timestamp


class UserHasRole(Timestamp, Base):
    __tablename__ = "user_has_role"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand.brand_id"), index=True)
    role_id = Column(Integer, ForeignKey("role.role_id"), index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profile.user_profile_id"), nullable=False)

    brand = relationship("Brand", backref="user_has_role")
    user_profile = relationship("UserProfile", backref="user_has_role")
    role = relationship("Role", backref="user_has_role")
