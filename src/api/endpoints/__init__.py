from fastapi import APIRouter
from src.api.endpoints.task import router as task

main_router = APIRouter()

main_router.include_router(task)

__all__ = ["main_router"]
