from app.models.employee_model import Employee, UserRole
from app.schemas.user_schema import Create_Emp,Login_Emp
from app.database.init_db import get_db
from app.core.hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from fastapi import  HTTPException, status
from app.core.tokens import create_access_token,create_refresh_token

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


async def login_emp(emp:Login_Emp, db: AsyncSession):
    query = select(Employee).where(Employee.emp_id == emp.emp_id)
    result = await db.execute(query)
    emp_obj = result.scalar_one_or_none()


    if not emp_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
        
    if not Hasher.verify_password(emp.password, emp_obj.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    access_token = create_access_token(emp_obj.emp_id, emp_obj.role.value)
    refresh_token = create_refresh_token(emp_obj.emp_id, emp_obj.role.value)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
    
    
async def get_employee_name(emp_id,db: AsyncSession):
    query = select(Employee.emp_name).where(Employee.emp_id == emp_id)
    result = await db.execute(query)
    employee_name = result.scalar()
    if employee_name:
        return {"emp_name": employee_name}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )