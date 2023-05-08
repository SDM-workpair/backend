import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.base_class import Base


class NotificationTemplate(Base):
    __tablename__ = "NotificationTemplate"
    template_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    template_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
