from fastapi import APIRouter, Depends, status, HTTPException 

from sqlalchemy.orm import Session

import uuid as uid

from app import crud, schemas

from app.clients.database import PostgresClient

router = APIRouter()


@router.post("/projects", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(PostgresClient.db)):
    new_project = crud.project.create(db, project)
    return new_project


@router.get("/projects/{project_id}", response_model=schemas.ProjectRead, status_code=status.HTTP_200_OK)
async def read_project(project_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    project = crud.project.read(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=schemas.ProjectRead, status_code=status.HTTP_200_OK)
async def update_project(project_id: uid.UUID, project_update: schemas.ProjectUpdate, db: Session = Depends(PostgresClient.db)):
    project = crud.project.update(db, project_id, project_update)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uid.UUID, db: Session = Depends(PostgresClient.db)):
    success = crud.project.delete(db, project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return None 


@router.get("/projects/{project_id}/tasks", response_model=schemas.TaskPagination, status_code=status.HTTP_200_OK)
async def list_tasks_by_project_id(project_id: uid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(PostgresClient.db)):
    tasks = crud.task.list_by_foreign_key(db, "project_id", project_id, skip=skip, limit=limit)
    count = crud.task.count_by_foreign_key(db, "project_id", project_id)
    return {"total": count, "items": tasks}
