from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Pagination(BaseModel):
    limit: int | None = 100
    offset: int | None = 0


class TaskResponse(BaseModel):
    id: int | None
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime | None


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus


class TaskCreateResponse(BaseModel):
    task_id: int


class UpdateTaskSchema(BaseModel):
    task_id: int
    status: TaskStatus
