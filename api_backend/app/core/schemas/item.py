from enum import Enum

from pydantic import BaseModel


class ItemStatus(str, Enum):
    NOT_ACTIVATED = "not_activated"
    ACTIVATED = "activated"
    LISTED = "listed"
    LOCKED = "locked"
    BURNED = "burned"


class ItemCreation(BaseModel):
    """
    class needed during item creation
    """

    serial_number: str
    product_number: str
    config_decription_json: object


class ItemInfo(BaseModel):
    brand_name: str
    category_name: str
    item_class_name: str
    item_class_description: str
    product_number: str
    item_config_description: object
    activation_key: str
    image_hash_key: str
    serial_number: str
    status: str


class ItemTransfered(ItemInfo):
    transfered_to_username: str


class ItemDeletion(ItemInfo):
    burn_status: bool
    delete_status: bool
