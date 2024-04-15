from pydantic import BaseModel


class Right(BaseModel):
    right_id: int
    right_name: str

    class Config:
        orm_mode = True
