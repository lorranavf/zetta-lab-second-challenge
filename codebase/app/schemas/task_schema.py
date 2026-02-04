import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .default import PaginatedResponse


class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: uuid.UUID
    due_date: datetime | None = None


class TaskRead(BaseModel):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    completed_at: datetime | None = None
    archived_at: datetime | None = None
    due_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskPagination(PaginatedResponse[TaskRead]):
    pass
