
import uuid

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from typing import Optional

class ProjectCreate(BaseModel):

    title: str
    description: str
    user_id: uuid.UUID


class ProjectRead(BaseModel):

    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ProjectDelete(BaseModel):

    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)





