"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class NotificationBase(BaseModel):
    pass


# Properties to receive via API on creation


class NotificationCreate(NotificationBase):
    receiver_uuid: UUID
    sender_uuid: UUID
    send_time: datetime
    template_uuid: UUID
    f_string: str


# Properties to receive via API on update


class NotificationUpdate(NotificationBase):
    pass


class NotificationInDBBase(NotificationBase):
    receiver_uuid: UUID
    sender_uuid: UUID
    send_time: datetime
    template_uuid: UUID
    f_string: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class Notification(NotificationInDBBase):
    pass


# Additional properties stored in DB
class NotificationInDB(NotificationInDBBase):
    notification_uuid: UUID


class NotificationViewModel(BaseModel):
    receiver_uuid: UUID
    send_time: datetime
    content: str


class NotificationTextWithMessage(BaseModel):
    message: str
    data: Optional[List[NotificationViewModel]] = None


class NotificationSendObjectModel(BaseModel):
    receiver_uuid: UUID
    sender_uuid: UUID
    template_uuid: UUID
    f_string: str
