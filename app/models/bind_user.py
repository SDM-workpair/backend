import uuid

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class BindUser(Base):
    __tablename__ = "BindUser"
    bind_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    bind_time = Column(DateTime(timezone=True), default=func.now())
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MatchingRoom.room_uuid", ondelete="CASCADE"),
        nullable=False,
    )
