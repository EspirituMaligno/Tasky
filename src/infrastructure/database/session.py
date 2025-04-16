from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio

from config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()
