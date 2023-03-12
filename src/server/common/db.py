from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.server.config import DBConfig

SyncEngine = create_engine(DBConfig.URL)
AsyncEngine = create_async_engine(DBConfig.URL)

SessionLocal = sessionmaker(
    bind=AsyncEngine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session
