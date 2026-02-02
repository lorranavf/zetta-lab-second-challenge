from models.task import Task
from .default import GenericCRUD

from schemas.task_schema import TaskCreate, TaskUpdate

task = GenericCRUD[Task, TaskCreate, TaskUpdate](Task)