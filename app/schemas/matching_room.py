"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class MatchingRoomBase(BaseModel):
    room_id: str


# Properties to receive via API on creation
class MatchingRoomReq(BaseModel):
    name: Optional[str] = None
    due_time: datetime
    min_member_num: int
    description: Optional[str] = None
    is_forced_matching: bool = False


class MatchingRoomCreate(MatchingRoomBase):
    name: Optional[str] = None
    due_time: datetime
    min_member_num: int
    description: Optional[str] = None
    is_forced_matching: bool = False
    created_time: datetime = None


# Properties to receive via API on update


class MatchingRoomUpdate(MatchingRoomBase):
    pass


class MatchingRoomInDBBase(MatchingRoomBase):
    name: Optional[str]
    room_id: str
    due_time: datetime
    min_member_num: int
    description: Optional[str] = None
    is_forced_matching: bool = False
    created_time: datetime = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class MatchingRoom(MatchingRoomInDBBase):
    pass


# Additional properties stored in DB
class MatchingRoomInDB(MatchingRoomInDBBase):
    room_uuid: UUID
    is_closed: bool = False
    finish_time: datetime


class MatchingRoomWithMemberID(MatchingRoom):
    member_id: Optional[int]


class MatchingRoomsWithMessage(BaseModel):
    message: str
    data: Optional[List[MatchingRoomWithMemberID]] = None


class MatchingRoomWithMessage(BaseModel):
    message: str
    data: Optional[MatchingRoom] = None


class MatchingRoomWithRoomId(BaseModel):
    message: str
    room_id: str


class MatchingRoomWithSearch(BaseModel):
    prompt: str
    query_all: bool


# For Demo
class MatchingRoomForEvent(MatchingRoomBase):
    group_choice: str = "random"
    slot_choice: str = "fixed_min"
    proximity: bool = True
    num_groups: int = None
    max_users: int = None
    min_users: int = None
