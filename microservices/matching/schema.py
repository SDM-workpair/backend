from enum import Enum
from typing import List

from loguru import logger
from pydantic import BaseModel, validator


class GroupChoice(str, Enum):
    random = "random"
    similarity = "similarity"
    tinder = "tinder"


class SlotChoice(str, Enum):
    fixed_group = "fixed_group"
    fixed_max = "fixed_max"
    fixed_min = "fixed_min"


class Params(dict):
    num_groups: int = None
    max_users: int = None
    min_users: int = None


class MatchingEvent(BaseModel):
    room_id: str
    group_choice: GroupChoice = "random"
    slot_choice: SlotChoice = "fixed_group"
    proximity: bool = True
    params: Params = {"num_groups": 3, "max_users": 6, "min_users": 3}

    @validator("params")
    def check_exist_one(cls, v, values):
        vals = v.values()
        for val in vals:
            if not isinstance(val, int) or val < 0:
                logger.error(f"params value must be positive integer, params: {v}")
                raise ValueError("params value must be positive integer")
        p = v.keys()
        if "num_groups" not in p and "max_users" not in p and "min_users" not in p:
            logger.error(
                f"Please provice one of the following params: num_groups, max_users, min_users. params: {p}"
            )
            raise ValueError(
                "Please provice one of the following params: num_groups, max_users, min_users"
            )
        return v


class MatchingGroups(BaseModel):
    groups: dict[str, List[int]] = {}


class Message(BaseModel):
    message: str
