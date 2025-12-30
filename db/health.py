from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.pool import get_engine


async def check_database_health() -> bool:
    """Return True when the database responds to a simple probe."""
    engine = get_engine()
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False
