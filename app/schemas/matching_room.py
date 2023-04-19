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
    created_time: datetime = None

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
    is_closed: bool = False
    finish_time: datetime


class MatchingRoomsWithMessage(BaseModel):
    message: str
    data: Optional[List[MatchingRoom]] = None


class MatchingRoomWithMessage(BaseModel):
    message: str
    data: Optional[MatchingRoom] = None


class MatchingRoomWithSearch(BaseModel):
    user_email: str
    prompt: str
    query_all: bool
