"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from typing import List

from pydantic import BaseModel

from .matching_room import MatchingRoomBase


# Shared properties
class Tag_Base(BaseModel):
    tag_text: str
    matching_room: MatchingRoomBase


class Tag_Create(Tag_Base):
    pass


# Properties to receive via API on update
class Tag_Update(Tag_Base):
    pass


class Tag_InDBBase(Tag_Base):
    pass

    class Config:
        orm_mode = True


class Tag_Res(BaseModel):
    message: str
    data: List[str]
