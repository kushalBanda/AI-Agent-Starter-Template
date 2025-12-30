from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.db.types import AsyncSessionMaker


class DatabaseSettings(BaseSettings):
    """Database settings derived from environment variables."""

    model_config = SettingsConfigDict(env_prefix="DB_", case_sensitive=False, frozen=True)

    host: str = Field(default="localhost", min_length=1)
    port: int = Field(default=5432, ge=1, le=65535)
    name: str = Field(default="app", min_length=1)
    user: str = Field(default="app", min_length=1)
    password: str = Field(default="")
    pool_size: int = Field(default=10, ge=1)
    max_overflow: int = Field(default=20, ge=0)
    pool_timeout_seconds: int = Field(default=30, ge=1)
    pool_recycle_seconds: int = Field(default=1800, ge=0) 

    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        """Build settings from the configured environment."""
        return cls()

    def to_url(self) -> URL:
        """Create a SQLAlchemy URL for asyncpg."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


_engine: AsyncEngine | None = None
_sessionmaker: AsyncSessionMaker | None = None


def get_engine() -> AsyncEngine:
    """Return a singleton async engine configured for production use."""
    global _engine
    if _engine is None:
        settings = DatabaseSettings.from_env()
        _engine = create_async_engine(
            settings.to_url(),
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
            pool_timeout=settings.pool_timeout_seconds,
            pool_recycle=settings.pool_recycle_seconds,
            pool_pre_ping=True,
        )
    return _engine


def get_sessionmaker() -> AsyncSessionMaker:
    """Return a singleton sessionmaker bound to the shared engine."""
    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(
            bind=get_engine(),
            expire_on_commit=False,
            class_=AsyncSession,
        )
    return _sessionmaker


async def dispose_engine() -> None:
    """Close the engine and reset the pool for shutdown or tests."""
    global _engine, _sessionmaker
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _sessionmaker = None
