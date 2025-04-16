from fastapi import Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.jwt import decode_token
from src.core.entities.user import User
from src.core.use_cases.task import TaskUseCases
from src.core.use_cases.user import UserUseCases
from src.infrastructure.database.repositories.user import UserRepository
from src.core.interfaces.user import IUserRepository
from src.infrastructure.database.session import get_db
from src.infrastructure.database.repositories.task import TaskRepository
from src.core.interfaces.task import ITaskRepository


security = HTTPBearer()


async def get_task_repo(session: AsyncSession = Depends(get_db)) -> ITaskRepository:
    return TaskRepository(session)


async def get_task_usecases(
    repo: ITaskRepository = Depends(get_task_repo),
) -> TaskUseCases:
    return TaskUseCases(repo)


async def get_user_repo(session: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserRepository(session)


async def get_user_usecases(
    repo: IUserRepository = Depends(get_user_repo),
) -> UserUseCases:
    return UserUseCases(repo)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repo: IUserRepository = Depends(get_user_repo),
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user_orm = await repo.get_user_by_id(user_id)
    if not user_orm:
        raise HTTPException(status_code=404, detail="User not found")

    return User(
        id=user_orm.id,
        name=user_orm.name,
        surname=user_orm.surname,
        date_of_birth=user_orm.date_of_birth,
        age=user_orm.age,
        username=user_orm.username,
        password=user_orm.password,
        is_active=user_orm.is_active,
        created_at=user_orm.created_at,
    )
