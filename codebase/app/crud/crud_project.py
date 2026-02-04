from app.models.project import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate

from .default import GenericCRUD

project = GenericCRUD[Project, ProjectCreate, ProjectUpdate](Project)
