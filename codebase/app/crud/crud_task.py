from app.models.task import Task
from .default import GenericCRUD

from app.schemas.task_schema import TaskCreate, TaskUpdate

task = GenericCRUD[Task, TaskCreate, TaskUpdate](Task)