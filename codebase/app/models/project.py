import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.clients.database import PostgresClient

Base = PostgresClient.base()


class ProjectStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    status = Column(String, default=ProjectStatus.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    archived_at = Column(DateTime, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # relationships
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
