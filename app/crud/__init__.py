from .crud_gr_member import gr_member
from .crud_group import group
from .crud_matching_room import matching_room
from .crud_mr_member import mr_member
from .crud_mr_member_tag import mr_member_tag
from .crud_notification import notification
from .crud_notification_template import notification_template
from .crud_swipe_card import swipe_card
from .crud_tag import tag
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
