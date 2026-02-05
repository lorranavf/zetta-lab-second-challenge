import uuid

from pydantic import BaseModel, ConfigDict

from .default import PaginatedResponse


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    firstname: str
    lastname: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserPagination(PaginatedResponse[UserRead]):
    pass
