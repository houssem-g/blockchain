from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class ItemConfiguration(BaseModel):
    product_number: str = Form(...)
    description_json: object = Form(...)
    brand_name: str = Form(...)


class ItemConfigurationInfo(BaseModel):
    brand_name: str
    category_name: str
    item_class_name: str
    item_class_description: str
    product_number: str
    item_config_description: object
    image_hash: str
    image_size: Optional[int]
    properties_hash: str


class ItemConfigurationDeletion(ItemConfigurationInfo):
    delete_status: bool
