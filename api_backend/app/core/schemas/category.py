from pydantic import BaseModel


class CategoryBase(BaseModel):
    category_name: str

    class Config:
        orm_mode = True


class CategoryDeletion(CategoryBase):
    delete_status: bool
