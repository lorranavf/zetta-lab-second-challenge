from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.security import SecurityService

from .default import GenericCRUD


class UserCRUD(GenericCRUD[User, UserCreate, UserUpdate]):
    def before_create(self, data) -> dict:
        if "password" in data:
            data["password"] = SecurityService.hash_password(data["password"])
        return data

    def before_update(self, data) -> dict:
        if "password" in data:
            data["password"] = SecurityService.hash_password(data["password"])
        return data

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(self.model).filter(self.model.email == email).first()


user = UserCRUD(User)
