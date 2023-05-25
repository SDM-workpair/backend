import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class Notification(Base):
    __tablename__ = "Notification"
    notification_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    receiver_uuid = Column(
        UUID(as_uuid=True), ForeignKey("User.user_uuid"), nullable=False
    )
    sender_uuid = Column(UUID(as_uuid=True), ForeignKey("User.user_uuid"))
    send_time = Column(DateTime(timezone=True), nullable=False, default=func.now())
    template_uuid = Column(String, nullable=False)
    f_string = Column(String)
    is_read = Column(Boolean, nullable=False, default=False)
    group_id = Column(String, nullable=True)
