
import uuid

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from typing import Optional

from .default import PaginatedResponse


class TaskCreate(BaseModel):

    title: str
    description: str
    project_id: uuid.UUID
    due_date: Optional[datetime] = None


class TaskRead(BaseModel):

    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TaskPagination(PaginatedResponse[TaskRead]):
    pass


