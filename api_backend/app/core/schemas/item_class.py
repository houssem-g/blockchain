from pydantic import BaseModel


class ItemClassInput(BaseModel):
    product_number: str
    name: str
    description: str
    category_name: str
    brand_name: str

    class Config:
        orm_mode = True


class ItemClassInfo(BaseModel):
    product_number: str
    name: str
    description: str
    category_name: str
    brand_name: str


class ItemClassDeletion(ItemClassInfo):
    delete_status: bool
