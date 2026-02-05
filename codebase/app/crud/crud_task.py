from app.models.task import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate

from .default import GenericCRUD

task = GenericCRUD[Task, TaskCreate, TaskUpdate](Task)
