from fastapi import APIRouter, Depends, Query

from src.core.entities.user import User
from src.core.use_cases.task import TaskUseCases
from src.api.dependencies import get_current_user, get_task_usecases
from src.api.schemas.task import (
    Pagination,
    TaskResponse,
    TaskCreateSchema,
    UpdateTaskSchema,
)
from src.core.entities.task import Task


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", summary="Получить все таски", response_model=list[TaskResponse])
async def get_all_tasks(
    pagination: Pagination = Query(...),
    use_case: TaskUseCases = Depends(get_task_usecases),
    current_user: User = Depends(get_current_user),
):
    return await use_case.get_all_tasks(pagination.limit, pagination.offset)


@router.post("/", summary="Создать задачу", response_model=TaskResponse)
async def create_task(
    task: TaskCreateSchema,
    use_case: TaskUseCases = Depends(get_task_usecases),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(title=task.title, description=task.description, status=task.status)
    created_task = await use_case.create_task(new_task)

    return created_task


@router.patch("/", summary="Обновить статус таски", response_model=TaskResponse)
async def update_status_task(
    update_data: UpdateTaskSchema,
    use_case: TaskUseCases = Depends(get_task_usecases),
    current_user: User = Depends(get_current_user),
):
    return await use_case.update_task_status(update_data.task_id, update_data.status)
