# from app.database.base_class import Base
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from swipecard.database import Base


class MR_Rcmed_Member(Base):
    __tablename__ = "MR_Rcmed_Member"
    member_id = Column(
        Integer,
        ForeignKey("MR_Member.member_id"),
        primary_key=True,
        nullable=False,
    )
    rcmed_member_id = Column(
        Integer,
        ForeignKey("MR_Member.member_id"),
        primary_key=True,
        nullable=False,
    )
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MatchingRoom.room_uuid"),
        nullable=False,
    )
    order = Column(Integer, nullable=False)
