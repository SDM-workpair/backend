import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class MatchingEvent(Base):
    __tablename__ = "MatchingEvent"
    matching_event_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    maching_algo = Column(String, nullable=False, default="random")
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False
    )
