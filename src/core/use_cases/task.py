from src.core.entities.task import Task
from src.core.interfaces.task import ITaskRepository


class TaskUseCases:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    async def get_all_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        return await self.repo.get_all(limit, offset)

    async def create_task(self, task: Task) -> Task:
        return await self.repo.create(task)

    async def update_task_status(self, task_id: int, status: str) -> Task:
        return await self.repo.change_status(task_id, status)
