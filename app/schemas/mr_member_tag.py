"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from .user import UserBase
from .matching_room import MatchingRoomBase
from .mr_member import MR_Member_Base
# from sqlalchemy import ARRAY


# Shared properties
class MR_Member_Tag_Base(BaseModel):
    mr_member: MR_Member_Base
    tag_text_list: List[str]

# Properties to receive via API on creation
# class MR_Member_Tag_Req(MR_Member_Tag_Base):
#     user: UserBase
#     matching_room: MatchingRoomBase

class MR_Member_Tag_Create(MR_Member_Tag_Base):
    matching_room: MatchingRoomBase


# Properties to receive via API on update
class MR_Member_Tag_Update(MR_Member_Tag_Base):
    pass


class MR_Member_Tag_InDBBase(MR_Member_Tag_Base):
    pass

    class Config:
        orm_mode = True


# Additional properties to return via API
class MR_Member_Tag(MR_Member_Tag_Base):
    pass

class MR_Member_Tag_Res(BaseModel):
    message: str
    data: List[str]


