import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.base_class import Base


class Tag(Base):
    __tablename__ = "Tag"
    tag_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    tag_text = Column(String, unique=True, nullable=False)
    room_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("MatchingRoom.room_uuid"),
        primary_key=True,
        nullable=False,
    )
    mentioned_num = Column(Integer, nullable=False, default=0)
