from fastapi import APIRouter
from src.api.endpoints.task import router as task
from src.api.endpoints.auth import router as auth
from src.api.endpoints.users import router as users

main_router = APIRouter()

main_router.include_router(task)
main_router.include_router(auth)
main_router.include_router(users)

__all__ = ["main_router"]
