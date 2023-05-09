"""
BaseModel.schema will return a dict of the schema
while BaseModel.schema_json will return a JSON string representation of that dict.
"""
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class NotificationTemplateBase(BaseModel):
    pass


# Properties to receive via API on creation


class NotificationTemplateCreate(NotificationTemplateBase):
    text: str


# Properties to receive via API on update


class NotificationTemplateUpdate(NotificationTemplateBase):
    pass


class NotificationTemplateInDBBase(NotificationTemplateBase):
    text: str

    class Config:
        orm_mode = True


# Additional properties to return via API
class NotificationTemplate(NotificationTemplateInDBBase):
    pass


# Additional properties stored in DB
class NotificationTemplateInDB(NotificationTemplateInDBBase):
    template_uuid: UUID
