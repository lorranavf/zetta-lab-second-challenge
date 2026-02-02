from sqlalchemy.orm import Session

import uuid

import schemas, models


def create_project(db: Session, project: schemas.ProjectCreate) -> schemas.ProjectRead:

    db_project = models.Project(
        name=project.name,
        description=project.description,
        user_id=project.user_id,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def read_project(db: Session, project_id: uuid.UUID) -> schemas.ProjectRead | None:

    return db.query(models.Project).filter(models.Project.id == project_id).first()


def update_project(db: Session, project_id: uuid.UUID, project_update: schemas.ProjectUpdate) -> schemas.ProjectRead | None:

    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not db_project:
        return None

    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: uuid.UUID) -> bool:

    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not db_project:
        return False

    db.delete(db_project)
    db.commit()

    return True

def list_projects_by_user_id(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[schemas.ProjectRead]:

    return db.query(models.Project).filter(models.Project.user_id == user_id).offset(skip).limit(limit).all()