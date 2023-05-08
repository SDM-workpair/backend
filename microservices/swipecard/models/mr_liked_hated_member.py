# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from microservices.swipecard.database import Base

from .matching_room import MatchingRoom
from .mr_member import MR_Member


class MR_Liked_Hated_Member(Base):
    __tablename__ = "MR_Liked_Hated_Member"
    member_id = Column(
        Integer,
        ForeignKey(MR_Member.member_id),
        primary_key=True,
        nullable=False,
    )
    target_member_id = Column(
        Integer,
        ForeignKey(MR_Member.member_id),
        primary_key=True,
        nullable=False,
    )
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey(MatchingRoom.room_uuid),
        nullable=False,
    )
    is_liked = Column(Boolean, nullable=False, default=False)
    is_hated = Column(Boolean, nullable=False, default=False)
