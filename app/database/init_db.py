from app.database.base import Async_session
from app.models.employee_model import Employee
async def get_db():
    async with Async_session() as session:
        yield session
        