from typing import Generic, TypeVar, List
from pydantic import BaseModel

ModelType = TypeVar("ModelType")

class PaginatedResponse(BaseModel, Generic[ModelType]):
    total: int
    items: List[ModelType]