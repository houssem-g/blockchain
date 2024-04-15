from datetime import datetime

from fastapi import Form
from pydantic import BaseModel


class RouteLoggingBase(BaseModel):

    route_url: str
    request_method: str
    host: str
    response: object = Form(...)
    current_user_profile_id: int
    brand_id: int
    process_time: float

    class Config:
        orm_mode = True


class RouteLogging(RouteLoggingBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
