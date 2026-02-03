from typing import Generic, Type, TypeVar, List, Optional, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class GenericCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def read(self, db: Session, id: Any) -> Optional[ModelType] :
        return db.get(self.model, id)
    
    def list(self, db: Session, skip: int = 0, limit: int = 100) ->  Optional[List[ModelType]]:
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def list_by_foreign_key(self, db: Session, fk_name: str, fk_value: Any, skip: int = 0, limit: int = 100) -> Optional[List[ModelType]]:
        return db.query(self.model).filter(getattr(self.model, fk_name) == fk_value).offset(skip).limit(limit).all()

    def create(self, db: Session, instance: CreateSchemaType) -> ModelType:
        db_obj = self.model(**instance.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: Any, instance: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = db.query(self.model).filter(self.model.id == id).first()

        if not db_obj:
            return None

        for key, value in instance.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(self, db: Session, id: Any) -> Any:
        db_obj = db.get(self.model, id)
        if not db_obj:
            return None
        db.delete(db_obj)
        db.commit()
        return id
    
    def count(self, db: Session) -> int:
        return db.query(self.model).count()
    
    def count_by_foreign_key(self, db: Session, fk_name: str, fk_value: Any) -> int:
        return db.query(self.model).filter(getattr(self.model, fk_name) == fk_value).count()