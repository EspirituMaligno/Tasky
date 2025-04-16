from abc import ABC, abstractmethod
from src.core.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_user_by_filters(self, **filters_by) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        pass
