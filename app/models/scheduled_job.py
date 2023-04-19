import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base_class import Base


class ScheduledJob(Base):
    __tablename__ = "ScheduledJob"
    job_uuid = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    trigger_time = Column(DateTime(timezone=True), nullable=False, default=func.now())
