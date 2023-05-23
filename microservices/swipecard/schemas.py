from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class SwipeCardBase(BaseModel):
    member_id: str = None
    room_id: str = None


class SwipeCardCreate(SwipeCardBase):
    recommended_member_id: str


# Properties to receive via API on update
class SwipeCardUpdate(SwipeCardBase):
    pass


class SwipeCardInDBBase(SwipeCardBase):
    recommended_member_id: str
    self_tag_text: Optional[List[str]]
    find_tag_text: Optional[List[str]]
    image: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True


class SwipeCard(SwipeCardInDBBase):
    pass


class SwipeCardInDB(SwipeCardInDBBase):
    pass

    class Config:
        orm_mode = True


# ask for recommendation
class SwipeCardAskRecommend(SwipeCardBase):
    pass


class SwipeCardRecommend(SwipeCardBase):
    recommended_member_id: str


class SwipeCardPreference(SwipeCardBase):
    target_member_id: str = None
    is_liked: bool = True
    is_hated: bool = False

    class Config:
        orm_mode = True


class SwipeCardMessage(BaseModel):
    message: str
    data: Optional[List[SwipeCard]] = None


class SwipeCardPreferenceMessage(BaseModel):
    message: str
    data: Optional[SwipeCardPreference] = None
