from fastapi import APIRouter, Depends, status, HTTPException 

from sqlalchemy.orm import Session

import uuid as uid

from app import crud, schemas

from app.clients.database import PostgresClient


router = APIRouter()


@router.get("/users", response_model=schemas.UserPagination, status_code=status.HTTP_200_OK)
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(PostgresClient.db)):
    users = crud.user.list(db, skip=skip, limit=limit)
    count = crud.user.count(db)
    return {"total": count, "items": users}

@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(PostgresClient.db)):
    new_user = crud.user.create(db, user)
    return new_user

@router.get("/users/{user_id}", response_model=schemas.UserRead, status_code=status.HTTP_200_OK)
async def read_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    user = crud.user.read(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserRead, status_code=status.HTTP_200_OK)
async def update_user(user_id: uid.UUID, user_update: schemas.UserUpdate, db: Session = Depends(PostgresClient.db)):
    user = crud.user.update(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    success = crud.user.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None


@router.get("/users/{user_id}/projects", response_model=schemas.ProjectPagination, status_code=status.HTTP_200_OK)
async def list_projects_by_user_id(user_id: uid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(PostgresClient.db)):
    projects = crud.project.list_by_foreign_key(db, "user_id", user_id, skip=skip, limit=limit)
    count = crud.project.count_by_foreign_key(db, "user_id", user_id)
    return {"total": count, "items": projects}
