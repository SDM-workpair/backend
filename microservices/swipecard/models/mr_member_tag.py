# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from microservices.swipecard.database import Base


class MR_Member_Tag(Base):
    __tablename__ = "MR_Member_Tag"
    member_id = Column(
        Integer,
        ForeignKey("MR_Member.member_id"),
        primary_key=True,
        nullable=False,
    )
    tag_text = Column(String, primary_key=True, nullable=False)
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MatchingRoom.room_uuid"),
        nullable=False,
    )
    is_self_tag = Column(Boolean, nullable=False, default=False)
    is_find_tag = Column(Boolean, nullable=False, default=False)
