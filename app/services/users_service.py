from app.models.employee_model import Employee, UserRole
from app.schemas.user_schema import Create_Emp
from app.database.init_db import get_db
from app.core.hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from fastapi import  HTTPException, status

async def create_emp(emp: Create_Emp, db: AsyncSession):
    query = select(Employee).where(Employee.emp_id == emp.emp_id)
    result = await db.execute(query)
    existing_emp = result.scalar_one_or_none()

    if existing_emp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already exists")

    emp_obj = Employee(
        emp_id = emp.emp_id,
        emp_name = emp.emp_name,
        password = Hasher.get_password_hash(emp.password),
        role = UserRole(emp.role)
    )

    db.add(emp_obj)
    await db.commit()
    await db.refresh(emp_obj)
    return True
