from enum import Enum
from typing import List

from pydantic import BaseModel


class GroupChoice(str, Enum):
    random = "random"
    similarity = "similarity"
    tinder = "tinder"


class SlotChoice(str, Enum):
    fixed_group = "fixed_group"
    fixed_max = "fixed_max"
    fixed_min = "fixed_min"


class MatchingEvent(BaseModel):
    room_id: str
    group_choice: GroupChoice = "random"
    slot_choice: SlotChoice = "fixed_group"
    params: dict = {}


class MatchingGroups(BaseModel):
    groups: dict[str, List[int]] = {}


class Message(BaseModel):
    message: str
