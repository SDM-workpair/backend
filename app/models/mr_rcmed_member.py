import uuid
from app.database.base_class import Base
from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class MR_Rcmed_Member(Base):
    __tablename__ = "MR_Rcmed_Member"
    member_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MR_Member.member_uuid"), primary_key=True, nullable=False
    )
    rcmed_member_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MR_Member.member_uuid"), primary_key=True, nullable=False
    )
    room_uuid = Column(
        UUID(as_uuid=True), ForeignKey("MatchingRoom.room_uuid"), nullable=False
    )
    order = Column(Integer, nullable=False)