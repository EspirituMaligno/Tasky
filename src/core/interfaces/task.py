from abc import ABC, abstractmethod

from src.core.entities.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Task]:
        pass

    @abstractmethod
    async def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def change_status(self, id: int, status: str) -> Task:
        pass
