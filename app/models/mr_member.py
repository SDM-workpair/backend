import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class MR_Member(Base):
    __tablename__ = "MR_Member"
    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey("User.user_uuid"), primary_key=True, nullable=False
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), primary_key=True, nullable=False
    )
    member_uuid = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4
    )
    join_time = Column(DateTime(timezone=True), default=func.now())
    grouped_time = Column(DateTime(timezone=True)) #要改
    is_grouped = Column(Boolean, nullable=False, default=False) #要改
    is_bound = Column(Boolean, nullable=False, default=False)
    bind_uuid = Column(
        UUID(as_uuid=True), ForeignKey("BindUser.bind_uuid")
    )