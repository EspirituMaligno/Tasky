from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas.auth import (
    AuthResponseModel,
    TokenDataSchema,
    UserCreateSchema,
    UserLoginSchema,
)
from src.api.dependencies import get_refresh_token, get_user_usecases
from src.core.use_cases.user import UserUseCases


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", summary="Регистрация пользователя", response_model=AuthResponseModel
)
async def register(
    user_data: UserCreateSchema, use_case: UserUseCases = Depends(get_user_usecases)
):
    try:
        await use_case.register_user(
            name=user_data.name,
            surname=user_data.surname,
            date_of_birth=user_data.date_of_birth,
            username=user_data.username,
            raw_password=user_data.password,
        )
        return AuthResponseModel(
            status="201",
            message="User created successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/login", summary="Авторизация пользователя", response_model=TokenDataSchema
)
async def login(
    user_data: UserLoginSchema, use_case: UserUseCases = Depends(get_user_usecases)
):
    try:
        token_data = await use_case.authorize_user(
            username=user_data.username, raw_password=user_data.password
        )
        return TokenDataSchema(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/refresh", summary="Обновление токена", response_model=TokenDataSchema)
async def refresh(
    refresh_token: str = Depends(get_refresh_token),
    use_case: UserUseCases = Depends(get_user_usecases),
):
    tokens = await use_case.refresh_token(refresh_token)
    return TokenDataSchema(
        access_token=tokens["access_token"], refresh_token=tokens["refresh_token"]
    )
