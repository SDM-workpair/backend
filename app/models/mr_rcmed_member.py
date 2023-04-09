from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.database.base_class import Base


class MR_Rcmed_Member(Base):
    __tablename__ = "MR_Rcmed_Member"
    member_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MR_Member.member_uuid"),
        primary_key=True,
        nullable=False,
    )
    rcmed_member_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MR_Member.member_uuid"),
        primary_key=True,
        nullable=False,
    )
    order = Column(Integer, nullable=False)
