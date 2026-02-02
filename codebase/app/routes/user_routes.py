from fastapi import APIRouter, Depends, status, HTTPException 

from sqlalchemy.orm import Session

import uuid as uid

import crud, schemas

from clients.database import PostgresClient


router = APIRouter()


@router.get("/users", response_model=list[schemas.UserRead], status_code=status.HTTP_200_OK)
async def list_users(db: Session = Depends(PostgresClient.db)):
    users = crud.list_users(db)
    return users

@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(PostgresClient.db)):
    new_user = crud.create_user(db, user)
    return new_user

@router.get("/users/{user_id}", response_model=schemas.UserRead, status_code=status.HTTP_200_OK)
async def read_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    user = crud.read_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserRead, status_code=status.HTTP_200_OK)
async def update_user(user_id: uid.UUID, user_update: schemas.UserUpdate, db: Session = Depends(PostgresClient.db)):
    user = crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None


@router.get("/users/{user_id}/projects", response_model=list[schemas.ProjectRead], status_code=status.HTTP_200_OK)
async def list_projects_by_user_id(user_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    projects = crud.list_projects_by_user_id(db, user_id)
    return projects
