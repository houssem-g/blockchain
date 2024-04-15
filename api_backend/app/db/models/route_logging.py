from app.db.base import Base
from app.db.models.mixins import Timestamp
from sqlalchemy import (Column, Float, ForeignKey, Integer,  # type: ignore
                        String)
from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore


class RouteLogging(Timestamp, Base):
    __tablename__ = "route_logging"

    log_id = Column(Integer, primary_key=True, index=True)

    route_url = Column(String(250))
    request_method = Column(String(100))
    host = Column(String(250))
    response = Column(JSONB, nullable=True, server_default="{}")
    current_user_profile_id = Column(Integer, ForeignKey("user_profile.user_profile_id"), nullable=True)
    brand_id = Column(Integer, ForeignKey("brand.brand_id"), nullable=True)
    process_time = Column(Float)

    user = relationship("UserProfile", backref="route_logging")
    brand = relationship("Brand", backref="route_logging")
