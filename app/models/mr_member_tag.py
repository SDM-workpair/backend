import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class MR_Member_Tag(Base):
    __tablename__ = "MR_Member_Tag"
    member_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MR_Member.member_uuid"),
        primary_key=True,
        nullable=False,
    )
    tag_text = Column(String, nullable=False)
    is_self_tag = Column(Boolean, nullable=False, default=False)
    is_find_tag = Column(Boolean, nullable=False, default=False)
