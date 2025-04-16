from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task:
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at

    def mark_done(self):
        self.status = TaskStatus.DONE

    def to_response(self) -> dict:
        """Конвертирует в словарь для ответа API"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
        }
