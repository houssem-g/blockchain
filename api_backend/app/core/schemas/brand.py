from pydantic import BaseModel


class BrandBase(BaseModel):
    brand_name: str
    logo_url: str
    website: str
    description: str

    class Config:
        orm_mode = True


class BrandDeletion(BrandBase):
    delete_status: bool
