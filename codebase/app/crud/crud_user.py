from models.user import User
from .default import GenericCRUD

from schemas.user_schema import UserCreate, UserUpdate

user = GenericCRUD[User, UserCreate, UserUpdate](User)

