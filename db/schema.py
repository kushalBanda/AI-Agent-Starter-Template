from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
