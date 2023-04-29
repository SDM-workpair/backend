"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class GR_MemberBase(BaseModel):
    pass


# Properties to receive via API on creation


class GR_MemberCreate(GR_MemberBase):
    member_id: int
    group_uuid: UUID
    join_time: datetime = None


# Properties to receive via API on update


class GR_MemberUpdate(GR_MemberBase):
    pass


class GR_MemberInDBBase(GR_MemberBase):
    member_id: int
    group_uuid: UUID
    join_time: datetime = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class GR_Member(GR_MemberInDBBase):
    pass


# Additional properties stored in DB
class GR_MemberInDB(GR_MemberInDBBase):
    pass


class GR_MemberWithSearch(BaseModel):
    group_id: str
