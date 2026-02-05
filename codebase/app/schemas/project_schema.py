import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.project import ProjectStatus

from .default import PaginatedResponse


class ProjectCreate(BaseModel):
    title: str
    description: str


class ProjectRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str
    status: ProjectStatus
    created_at: datetime
    completed_at: datetime | None = None
    archived_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    completed_at: datetime | None = None
    archived_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectPagination(PaginatedResponse[ProjectRead]):
    pass
