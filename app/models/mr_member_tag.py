from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.base_class import Base


class MR_Member_Tag(Base):
    __tablename__ = "MR_Member_Tag"
    member_id = Column(
        Integer,
        ForeignKey("MR_Member.member_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    tag_text = Column(String, primary_key=True, nullable=False)
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MatchingRoom.room_uuid", ondelete="CASCADE"),
        nullable=False,
    )
    is_self_tag = Column(Boolean, nullable=False, default=False)
    is_find_tag = Column(Boolean, nullable=False, default=False)
