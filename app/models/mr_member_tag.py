import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class MR_Member_Tag(Base):
    __tablename__ = "MR_Member_Tag"
    member_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MR_Member.member_uuid"), primary_key=True, nullable=False
    )
    tag_text = Column(String, primary_key=True, nullable=False)
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False
    )
    user_uuid = Column(
        UUID(as_uuid=True), ForeignKey("User.user_uuid"), nullable=False
    )
    is_self_tag = Column(Boolean, nullable=False, default=False)
    is_find_tag = Column(Boolean, nullable=False, default=False)