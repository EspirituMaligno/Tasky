from fastapi import APIRouter, Depends, Query

from src.api.dependencies import get_task_repo
from src.api.schemas.task import (
    Pagination,
    TaskResponse,
    TaskCreateResponse,
    TaskCreateSchema,
    UpdateTaskSchema,
)
from src.core.interfaces.task import ITaskRepository
from src.core.entities.task import Task


router = APIRouter(prefix="/tasks")


@router.get("/", summary="Получить все таски", response_model=list[TaskResponse])
async def get_all_tasks(
    pagination: Pagination = Query(...), repo: ITaskRepository = Depends(get_task_repo)
):
    return await repo.get_all(pagination.limit, pagination.offset)


@router.post("/", summary="Создать задачу", response_model=TaskResponse)
async def create_task(
    task: TaskCreateSchema, repo: ITaskRepository = Depends(get_task_repo)
):
    new_task = Task(title=task.title, description=task.description, status=task.status)
    created_task = await repo.create(new_task)

    return created_task


@router.patch("/", summary="Обновить статус таски", response_model=TaskResponse)
async def update_status_task(
    update_data: UpdateTaskSchema,
    repo: ITaskRepository = Depends(get_task_repo),
):
    return await repo.change_status(update_data.task_id, update_data.status)
