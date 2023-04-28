import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


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


"""
Matching event scheduler
"""

from sqlalchemy import event
import loguru
from app.core.scheduler.matching_event import matching_event

@event.listens_for(MatchingRoom, 'after_insert')
def receive_after_insert(mapper, connection, target):
    "listen for the 'after_insert' event"
    # loguru.logger.info(mapper)
    # loguru.logger.info(connection)
    # loguru.logger.info(target.due_time)
    matching_event(target.due_time)
    
    # ... (event handling logic) ...