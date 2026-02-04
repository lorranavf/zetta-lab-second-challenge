import uuid as uid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.clients.database import PostgresClient
from app.services.authentication import AuthenticationService as AuthService

router = APIRouter()


@router.post(
    "/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED
)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    new_task = crud.task.create(db, task, current_user)
    return new_task


@router.get(
    "/tasks/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK
)
async def read_task(
    task_id: uid.UUID,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    task = crud.task.read(db, task_id, current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.put(
    "/tasks/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: uid.UUID,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    task = crud.task.update(db, task_id, task_update, current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uid.UUID,
    db: Session = Depends(PostgresClient.db),
    current_user: schemas.UserRead = Depends(AuthService.get_current_user),
):
    success = crud.task.delete(db, task_id, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return None
