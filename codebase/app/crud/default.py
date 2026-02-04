import builtins
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class GenericCRUD[ModelType, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel]:
    def __init__(self, model: type[ModelType]):
        self.model = model

    def validate_owner(self, db: Session, id: Any, current_user: Any = None) -> bool:
        obj = db.get(self.model, id)

        if not obj:
            return False

        if self.model.__name__ == "User":
            if obj.id != current_user.id:
                return False

        if hasattr(self.model, "user_id"):
            return obj.user_id == current_user.id

        return True

    def validate_query(self, query: Any, current_user: Any = None) -> Any:
        if not current_user:
            return query
        if self.model.__name__ == "User":
            return query.filter(self.model.id == current_user.id)
        if hasattr(self.model, "user_id"):
            return query.filter(self.model.user_id == current_user.id)
        return query

    def read(self, db: Session, id: Any, current_user: Any = None) -> ModelType | None:
        query = db.query(self.model).filter(self.model.id == id)
        query = self.validate_query(query, current_user)
        return query.first()

    def list(
        self, db: Session, skip: int = 0, limit: int = 100, current_user: Any = None
    ) -> list[ModelType] | None:
        query = db.query(self.model)
        query = self.validate_query(query, current_user)
        return query.offset(skip).limit(limit).all()

    def list_by_foreign_key(
        self,
        db: Session,
        fk_name: str,
        fk_value: Any,
        skip: int = 0,
        limit: int = 100,
        current_user: Any = None,
    ) -> builtins.list[ModelType] | None:
        query = db.query(self.model).filter(getattr(self.model, fk_name) == fk_value)
        query = self.validate_query(query, current_user)
        return query.offset(skip).limit(limit).all()

    def count(self, db: Session, current_user: Any = None) -> int:
        query = db.query(self.model)
        query = self.validate_query(query, current_user)
        return query.count()

    def count_by_foreign_key(
        self, db: Session, fk_name: str, fk_value: Any, current_user: Any = None
    ) -> int:
        query = db.query(self.model).filter(getattr(self.model, fk_name) == fk_value)
        query = self.validate_query(query, current_user)
        return query.count()

    def before_create(self, data: dict) -> dict:
        return data

    def create(
        self, db: Session, instance: CreateSchemaType, current_user: Any = None
    ) -> ModelType:
        data = self.before_create(instance.model_dump())

        if hasattr(self.model, "user_id") and current_user:
            data["user_id"] = current_user.id

        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def before_update(self, data: dict) -> dict:
        return data

    def update(
        self, db: Session, id: Any, instance: UpdateSchemaType, current_user: Any = None
    ) -> ModelType | None:
        if not self.validate_owner(db, id, current_user):
            return None

        db_obj = db.get(self.model, id)

        data = self.before_update(instance.model_dump(exclude_unset=True))

        for key, value in data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(self, db: Session, id: Any, current_user: Any = None) -> Any:
        if not self.validate_owner(db, id, current_user):
            return None

        db_obj = db.get(self.model, id)

        db.delete(db_obj)
        db.commit()
        return id
