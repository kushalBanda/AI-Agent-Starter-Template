from __future__ import annotations

from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.pool import get_sessionmaker
from app.db.types import AsyncSessionMaker


class UnitOfWork:
    """Unit of work that manages a transactional async session."""

    def __init__(self, sessionmaker: AsyncSessionMaker | None = None) -> None:
        self._sessionmaker = sessionmaker or get_sessionmaker()
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        """Open a new session for the transaction boundary."""
        self.session = self._sessionmaker()
        return self.session

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: object | None,
    ) -> None:
        """Commit on success, otherwise roll back before closing."""
        if self.session is None:
            return
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()

    async def begin(self) -> Self:
        """Explicitly begin a unit of work outside a context manager."""
        await self.__aenter__()
        return self

    async def end(self, exc: BaseException | None = None) -> None:
        """End a unit of work created via begin/end."""
        await self.__aexit__(type(exc) if exc else None, exc, None)
