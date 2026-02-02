from sqlalchemy.orm import Session

import uuid

import schemas, models


def create_task(db: Session, task: schemas.TaskCreate, user_id: uuid.UUID) -> schemas.TaskRead:

    db_task = models.Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        due_date=task.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def read_task(db: Session, task_id: uuid.UUID) -> schemas.TaskRead | None:

    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: uuid.UUID, task_update: schemas.TaskUpdate) -> schemas.TaskRead | None:

    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

def delete_task(db: Session, task_id: uuid.UUID) -> bool:

    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return False

    db.delete(db_task)
    db.commit()

    return True

def list_tasks_by_project_id(db: Session, project_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[schemas.TaskRead]:

    return db.query(models.Task).filter(models.Task.project_id == project_id).offset(skip).limit(limit).all()