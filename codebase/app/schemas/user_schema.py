
import uuid

from pydantic import BaseModel, ConfigDict

from typing import List, Optional

from .default import PaginatedResponse

class UserCreate(BaseModel):

    firstname: str
    lastname: str
    email: str
    password: str

class UserRead(BaseModel):

    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):

    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):

    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserPagination(PaginatedResponse[UserRead]):
    pass

