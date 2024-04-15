from datetime import datetime

from sqlalchemy import Column, DateTime  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
