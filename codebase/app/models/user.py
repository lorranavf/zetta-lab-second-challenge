import uuid
from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.clients.database import PostgresClient

Base = PostgresClient.base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    created_at = Column(String, default=datetime.now)

    # relationships
    projects = relationship("Project", back_populates="user")
