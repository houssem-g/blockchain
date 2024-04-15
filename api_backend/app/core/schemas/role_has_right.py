from pydantic import BaseModel


class RoleHasRight(BaseModel):
    role_id: int
    right_id: int

    class Config:
        orm_mode = True
