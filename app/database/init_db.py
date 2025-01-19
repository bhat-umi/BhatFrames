from app.database.base import Async_session

async def get_db():
    async with Async_session() as session:
        yield session
        