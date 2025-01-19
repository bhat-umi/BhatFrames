from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker

base = declarative_base()

DATABASE_URL = f"postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"



engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
                             )
Async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
