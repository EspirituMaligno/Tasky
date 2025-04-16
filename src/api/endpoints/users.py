from fastapi import APIRouter, Depends

from src.api.dependencies import get_user_usecases
from src.core.use_cases.user import UserUseCases


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", summary="Получить пользователя по id")
async def get_one_user(
    user_id: int,
    use_case: UserUseCases = Depends(get_user_usecases),
):
    return await use_case.get_user_by_id(user_id)
