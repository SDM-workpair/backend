import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from microservices.models.base_class import Base


class MatchingRoom(Base):
    __tablename__ = "MatchingRoom"
    room_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name = Column(String, nullable=False)
    room_id = Column(String, unique=True, nullable=False)
    due_time = Column(DateTime(timezone=True), nullable=False)
    min_member_num = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    is_forced_matching = Column(Boolean, nullable=False, default=False)
    created_time = Column(DateTime(timezone=True), default=func.now())
    is_closed = Column(Boolean, nullable=False, default=False)
    finish_time = Column(DateTime(timezone=True), nullable=True)
