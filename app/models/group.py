import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class Group(Base):
    __tablename__ = "Group"
    group_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False
    )
    create_time = Column(DateTime(timezone=True), default=func.now())
    group_id = Column(String, nullable=False) #mr_id+數字
    name = Column(String, nullable=False)
