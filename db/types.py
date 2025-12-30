from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionMaker = async_sessionmaker[AsyncSession]
AsyncSessionFactory = Callable[[], AsyncSession]
