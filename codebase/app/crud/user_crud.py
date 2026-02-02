from sqlalchemy.orm import Session

import uuid

import schemas, models


def create_user(db: Session, user: schemas.UserCreate) -> schemas.UserRead:

    db_user = models.User(
        email=user.email,
        password=user.password,
        firstname=user.firstname,
        lastname=user.lastname
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def read_user(db: Session, user_id: uuid.UUID) -> schemas.UserRead | None:

    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: uuid.UUID, user_update: schemas.UserUpdate) -> schemas.UserRead | None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return None

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: uuid.UUID) -> bool:

    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return False

    db.delete(db_user)
    db.commit()

    return True


def list_users(db: Session) -> list[schemas.UserRead]:

    return db.query(models.User).all()
