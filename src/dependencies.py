from sqlalchemy.ext.asyncio import AsyncSession

from .database.base import session_factory


async def get_db() -> AsyncSession:
    async with session_factory() as session:
        yield session
