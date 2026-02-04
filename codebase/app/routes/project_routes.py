from fastapi import APIRouter, Depends, status, HTTPException 

from sqlalchemy.orm import Session

import uuid as uid

from app import crud, schemas

from app.clients.database import PostgresClient

from app.services.authentication import AuthenticationService as AuthService


router = APIRouter()


@router.post("/projects", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: Session = Depends(PostgresClient.db), current_user: schemas.UserRead = Depends(AuthService.get_current_user)):
    new_project = crud.project.create(db, project, current_user)
    return new_project


@router.get("/projects/{project_id}", response_model=schemas.ProjectRead, status_code=status.HTTP_200_OK)
async def read_project(project_id: uid.UUID, db: Session = Depends(PostgresClient.db), current_user: schemas.UserRead = Depends(AuthService.get_current_user)):
    project = crud.project.read(db, project_id, current_user)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=schemas.ProjectRead, status_code=status.HTTP_200_OK)
async def update_project(project_id: uid.UUID, project_update: schemas.ProjectUpdate, db: Session = Depends(PostgresClient.db), current_user: schemas.UserRead = Depends(AuthService.get_current_user)):
    project = crud.project.update(db, project_id, project_update, current_user)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uid.UUID, db: Session = Depends(PostgresClient.db), current_user: schemas.UserRead = Depends(AuthService.get_current_user)):
    success = crud.project.delete(db, project_id, current_user)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return None 


@router.get("/projects/{project_id}/tasks", response_model=schemas.TaskPagination, status_code=status.HTTP_200_OK)
async def list_tasks_by_project_id(project_id: uid.UUID, skip: int = 0, limit: int = 100, db: Session = Depends(PostgresClient.db), current_user: schemas.UserRead = Depends(AuthService.get_current_user)):
    tasks = crud.task.list_by_foreign_key(db, "project_id", project_id, skip=skip, limit=limit, current_user=current_user)
    count = crud.task.count_by_foreign_key(db, "project_id", project_id, current_user=current_user)
    return {"total": count, "items": tasks}
