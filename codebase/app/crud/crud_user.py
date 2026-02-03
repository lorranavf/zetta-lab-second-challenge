from app.models.user import User
from .default import GenericCRUD

from app.schemas.user_schema import UserCreate, UserUpdate

user = GenericCRUD[User, UserCreate, UserUpdate](User)

