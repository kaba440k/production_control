from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import func, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


class Base(DeclarativeBase):
    pass

# Создать engine
engine = create_async_engine(
    settings.database_url.unicode_string(),
    pool_size=settings.database_pool_size,
    echo=settings.debug,
)

# Создать session maker
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def dispose_engine() -> None:
    """Закрыть все соединения с БД."""
    await engine.dispose()