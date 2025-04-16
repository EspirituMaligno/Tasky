from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import UserORM
from src.core.entities.user import User
from src.core.interfaces.user import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_filters(self, **filters_by) -> User | None:
        res = await self.session.execute(select(UserORM).filter_by(**filters_by))
        user_orm = res.scalar_one_or_none()

        if user_orm is None:
            return None

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

    async def get_user_by_id(self, id: int) -> User:
        res = await self.session.execute(select(UserORM).where(UserORM.id == id))
        user_orm = res.scalar_one_or_none()

        if user_orm is None:
            return None

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

    async def create_user(self, user: User) -> User:
        user_orm = UserORM(
            name=user.name,
            surname=user.surname,
            date_of_birth=user.date_of_birth,
            age=user.age,
            username=user.username,
            password=user.password,
        )
        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)

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

    async def update_user(self, user: dict) -> User:
        user_orm = await self.session.execute(
            update(UserORM).where(UserORM.id == user.id).values(**user)
        )
        await self.session.commit()
        await self.session.refresh(user_orm)

        return User(
            id=user_orm.id,
            username=user_orm.username,
            password=user_orm.password,
            is_active=user_orm.is_active,
            created_at=user_orm.created_at,
        )
