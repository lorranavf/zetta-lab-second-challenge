import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.clients.database import PostgresClient
from app.services.authentication import AuthenticationService as AuthService

router = APIRouter()


@router.post(
    "/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(PostgresClient.db)
):
    new_user = crud.user.create(db, user)
    return new_user


@router.get(
    "/users", response_model=schemas.UserPagination, status_code=status.HTTP_200_OK
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    users = crud.user.list(db, skip=skip, limit=limit, current_user=current_user)
    count = crud.user.count(db, current_user=current_user)
    return {"total": count, "items": users}


@router.get(
    "/users/{user_id}", response_model=schemas.UserRead, status_code=status.HTTP_200_OK
)
async def read_user(
    user_id: uid.UUID,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    user = crud.user.read(db, user_id, current_user=current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put(
    "/users/{user_id}", response_model=schemas.UserRead, status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: uid.UUID,
    user_update: schemas.UserUpdate,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    user = crud.user.update(db, user_id, user_update, current_user=current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uid.UUID,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    success = crud.user.delete(db, user_id, current_user=current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return None


@router.get(
    "/users/{user_id}/projects",
    response_model=schemas.ProjectPagination,
    status_code=status.HTTP_200_OK,
)
async def list_projects_by_user_id(
    user_id: uid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    projects = crud.project.list_by_foreign_key(
        db, "user_id", user_id, skip=skip, limit=limit, current_user=current_user
    )
    count = crud.project.count_by_foreign_key(
        db, "user_id", user_id, current_user=current_user
    )
    return {"total": count, "items": projects}
