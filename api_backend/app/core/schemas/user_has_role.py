from pydantic import BaseModel


class UserHasRole(BaseModel):
    role_id: int
    user_profile_id: int
    brand_id: int

    class Config:
        orm_mode = True
