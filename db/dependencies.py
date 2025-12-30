from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.pool import get_sessionmaker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a single async session per request."""
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session
