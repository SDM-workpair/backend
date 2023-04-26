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


# Shared properties
class MR_Member_Base(BaseModel):
    member_id: str

# Properties to receive via API on creation
class MR_Member_Req(BaseModel):
    user: UserBase
    matching_room: MatchingRoomBase

class MR_Member_Create(MR_Member_Base):
    user: UserBase
    matching_room: MatchingRoomBase
    join_time: datetime = None

class MR_Member_Res_Base(MR_Member_Base):
    user: UserBase
    matching_room: MatchingRoomBase

class MR_Member_Res(BaseModel):
    message: str
    data: MR_Member_Res_Base

# Properties to receive via API on update
class MR_Member_Update(MR_Member_Base):
    pass


class MR_Member_InDBBase(MR_Member_Base):
    user: UserBase
    room: MatchingRoomBase
    join_time: datetime = None
    grouped_time: datetime
    is_grouped: bool
    is_bound: bool

    class Config:
        orm_mode = True


# Additional properties to return via API
class MR_Member(MR_Member_Base):
    pass


