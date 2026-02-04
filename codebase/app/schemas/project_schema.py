
import uuid

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from typing import Optional

from .default import PaginatedResponse

class ProjectCreate(BaseModel):

    title: str
    description: str


class ProjectRead(BaseModel):

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectPagination(PaginatedResponse[ProjectRead]):
    pass


