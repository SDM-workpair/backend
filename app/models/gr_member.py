import uuid

from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class GR_Member(Base):
    __tablename__ = "GR_Member"
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("User.user_uuid"),
        primary_key=True,
        nullable=False,
    )
    group_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("Group.group_uuid"),
        primary_key=True,
        nullable=False,
    )
    join_time = Column(DateTime(timezone=True), default=func.now())
