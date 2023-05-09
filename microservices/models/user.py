import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from microservices.models.base_class import Base


class User(Base):
    __tablename__ = "User"
    user_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name = Column(String, nullable=False, default="--")
    password = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    line_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    image = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_google_sso = Column(Boolean, nullable=True, default=False)
