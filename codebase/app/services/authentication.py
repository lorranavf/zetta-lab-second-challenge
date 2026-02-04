from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import crud
from app.clients.database import PostgresClient
from app.services.security import SecurityService


class AuthenticationService:
    AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
    AUTH_SCHEME_OPTIONAL = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

    @classmethod
    def credentials_exception(cls):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    @classmethod
    async def get_current_user(
        cls, token: str = Depends(AUTH_SCHEME), db: Session = Depends(PostgresClient.db)
    ):
        try:
            payload = jwt.decode(
                token,
                SecurityService.SECRET_KEY,
                algorithms=[SecurityService.ALGORITHM],
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise cls.credentials_exception()
            user = crud.user.read(db, id=UUID(user_id))
            if user is None:
                raise cls.credentials_exception()
            return user
        except JWTError:
            raise cls.credentials_exception() from None

    @classmethod
    async def get_current_user_optional(
        cls,
        token: str | None = Depends(AUTH_SCHEME_OPTIONAL),
        db: Session = Depends(PostgresClient.db),
    ):
        if not token:
            return None
        try:
            return await cls.get_current_user(token, db)
        except Exception:
            return None
