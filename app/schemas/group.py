"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class GroupBase(BaseModel):
    group_uuid: UUID


# Properties to receive via API on creation


class GroupCreate(GroupBase):
    name: str
    group_id: str
    room_uuid: UUID
    created_time: datetime = None


# Properties to receive via API on update


class GroupUpdate(GroupBase):
    pass


class GroupInDBBase(GroupBase):
    name: str
    group_id: str
    room_uuid: UUID
    created_time: datetime = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Group(GroupInDBBase):
    pass


# Additional properties stored in DB
class GroupInDB(GroupInDBBase):
    pass


class GroupWithMessage(BaseModel):
    message: str
    data: Optional[List[Group]] = None


class GroupWithSearch(BaseModel):
    user_email: str
    prompt: str
