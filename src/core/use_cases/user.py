from datetime import date
from fastapi import HTTPException
from src.core.services.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from src.core.services.age import calculate_age
from src.core.entities.user import User
from src.core.interfaces.user import IUserRepository
from src.core.services.password import hash_password, check_password


class UserUseCases:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def get_user_by_id(self, id: int) -> list[User]:
        return await self.repo.get_user_by_id(id)

    async def register_user(
        self,
        name: str,
        surname: str,
        date_of_birth: date,
        username: str,
        raw_password: str,
    ) -> User:
        password_hash = hash_password(raw_password)

        existing_user = await self.repo.get_user_by_filters(username=username)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        age = calculate_age(date_of_birth)

        new_user = User(
            name=name,
            surname=surname,
            date_of_birth=date_of_birth,
            age=age,
            username=username,
            password=password_hash,
        )

        return await self.repo.create_user(new_user)

    async def authorize_user(self, username: str, raw_password: str) -> dict[str, str]:
        existing_user = await self.repo.get_user_by_filters(username=username)

        if not existing_user:
            raise HTTPException(status_code=400, detail="User not found")

        if not check_password(raw_password, existing_user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        token = create_access_token(data={"sub": "tasky", "user_id": existing_user.id})

        refresh_token = create_refresh_token(
            data={"sub": "tasky", "user_id": existing_user.id}
        )

        return {
            "access_token": token,
            "refresh_token": refresh_token,
        }

    async def refresh_token(self, refresh_token: str) -> dict[str, str]:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401, detail="Invalid token type. Expected refresh token"
            )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )

        user = await self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        token = create_access_token(data={"sub": "tasky", "user_id": user_id})

        refresh_token = create_refresh_token(data={"sub": "tasky", "user_id": user_id})

        return {
            "access_token": token,
            "refresh_token": refresh_token,
        }
