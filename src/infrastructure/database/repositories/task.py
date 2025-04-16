from sqlalchemy import select, update
from src.core.interfaces.task import ITaskRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.entities.task import Task
from src.infrastructure.database.models import TaskORM


class TaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Task]:
        res = await self.session.execute(select(TaskORM).limit(limit).offset(offset))
        tasks = res.scalars().all()

        return [
            Task(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at,
            )
            for task in tasks
        ]

    async def create(self, task: Task) -> Task:
        task_orm = TaskORM(
            title=task.title,
            description=task.description,
            status=task.status,
        )
        self.session.add(task_orm)
        await self.session.commit()
        await self.session.refresh(task_orm)

        return Task(
            id=task_orm.id,
            title=task_orm.title,
            description=task_orm.description,
            status=task_orm.status,
            created_at=task_orm.created_at,
        )

    async def change_status(self, id: int, status: str) -> Task:
        stmt = await self.session.execute(
            update(TaskORM)
            .where(TaskORM.id == id)
            .values(status=status)
            .returning(TaskORM)
        )
        task_orm = stmt.scalar_one_or_none()

        return Task(
            id=task_orm.id,
            title=task_orm.title,
            description=task_orm.description,
            status=task_orm.status,
            created_at=task_orm.created_at,
        )
