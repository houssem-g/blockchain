from pydantic import BaseModel


class EmailConfirmationBase(BaseModel):
    email: str
    status: str
    code: str

    class Config:
        orm_mode = True
