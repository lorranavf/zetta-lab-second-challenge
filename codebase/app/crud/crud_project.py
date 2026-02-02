from models.project import Project
from .default import GenericCRUD

from schemas.project_schema import ProjectCreate, ProjectUpdate

project = GenericCRUD[Project, ProjectCreate, ProjectUpdate](Project)