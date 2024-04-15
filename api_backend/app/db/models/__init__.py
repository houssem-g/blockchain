from app.db.models.brand import Brand
from app.db.models.category import Category
from app.db.models.email_confirmation import EmailConfirmation
from app.db.models.item import Item
from app.db.models.item_class import ItemClass
from app.db.models.item_configuration import ItemConfig
from app.db.models.role import Role
from app.db.models.route_logging import RouteLogging
from app.db.models.user_has_role import UserHasRole
from app.db.models.user_profile import UserProfile

DB_MODELS = [
    Brand,
    Category,
    Item,
    ItemClass,
    ItemConfig,
    Role,
    UserProfile,
    UserHasRole,
    EmailConfirmation,
    RouteLogging,
]
