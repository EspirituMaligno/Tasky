from typing import Optional, Tuple
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.session import get_db
from src.infrastructure.database.repositories.task import TaskRepository
from src.core.interfaces.task import ITaskRepository


async def get_task_repo(db: AsyncSession = Depends(get_db)) -> ITaskRepository:
    return TaskRepository(db)
