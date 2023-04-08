import uuid

from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class NotificationTemplate(Base):
    __tablename__ = "NotificationTemplate"
    template_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    text = Column(String, nullable=False)
