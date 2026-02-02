from fastapi import APIRouter, Depends, status, HTTPException 

from sqlalchemy.orm import Session

import uuid as uid

import crud, schemas

from clients.database import PostgresClient

router = APIRouter()


@router.post("/task", response_model=schemas.TaskCreate, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(PostgresClient.db)):
    new_task = crud.create_task(db, task)
    return new_task

@router.get("/task/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK)
async def read_task(task_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    task = crud.read_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/task/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK)
async def update_task(task_id: uid.UUID, task_update: schemas.TaskUpdate, db: Session = Depends(PostgresClient.db)):
    task = crud.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None


