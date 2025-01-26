from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payment_model import Payment, PaymentMethod
from app.schemas.payment_schema import PaymentCreate
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import select, func, text
from app.models.employee_model import Employee
from app.models.customer_model import Customer
from fastapi import HTTPException, status


async def create_payment(db: AsyncSession, emp_id: str, payment_data: PaymentCreate):
    
    try:
        current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
        
        query = select(Employee).where(Employee.emp_id == emp_id)
        result = await db.execute(query)
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        print("payement data ", payment_data)
        
        payment = Payment(
            customer_id=payment_data.customer_id,
            employee_id=employee.emp_id,
            payment_amount=payment_data.amount,
            payment_method=PaymentMethod(payment_data.payment_method.value),  # Access enum value
            payment_uid=payment_data.payment_uid,
            comments=payment_data.comments,
            payment_date=payment_data.payment_date,  # Now handles date object directly
            created_at=current_time,
            updated_at=current_time,
        )
        db.add(payment)
        await db.commit()
        await db.refresh(payment)
        return payment   
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
