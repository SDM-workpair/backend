import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class MR_Liked_Hated_Member(Base):
    __tablename__ = "MR_Liked_Hated_Member"
    member_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MR_Member.member_uuid"), primary_key=True, nullable=False
    )
    target_member_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MR_Member.member_uuid"), primary_key=True, nullable=False
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False
    )
    is_liked = Column(Boolean, nullable=False, default=False)
    is_hated = Column(Boolean, nullable=False, default=False)
