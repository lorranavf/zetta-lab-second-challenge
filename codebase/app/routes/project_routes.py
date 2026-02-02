from fastapi import APIRouter, Depends, status, HTTPException 

from sqlalchemy.orm import Session

import uuid as uid

import crud, schemas

from clients.database import PostgresClient

router = APIRouter()


@router.post("/project", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(PostgresClient.db)):
    new_project = crud.create_project(db, project)
    return new_project


@router.get("/project/{project_id}", response_model=schemas.ProjectRead, status_code=status.HTTP_200_OK)
async def read_project(project_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    project = crud.read_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/project/{project_id}", response_model=schemas.ProjectRead, status_code=status.HTTP_200_OK)
async def update_project(project_id: uid.UUID, project_update: schemas.ProjectUpdate, db: Session = Depends(PostgresClient.db)):
    project = crud.update_project(db, project_id, project_update)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    success = crud.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return None 


@router.get("/project/{project_id}/tasks", response_model=list[schemas.TaskRead], status_code=status.HTTP_200_OK)
async def list_tasks_by_project_id(project_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    tasks = crud.list_tasks_by_project_id(db, project_id)
    return tasks
