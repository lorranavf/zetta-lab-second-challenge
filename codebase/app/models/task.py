import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.clients.database import PostgresClient

Base = PostgresClient.base()


class TaskStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    status = Column(String, default=TaskStatus.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    archived_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))

    # relationships
    project = relationship("Project", back_populates="tasks")
