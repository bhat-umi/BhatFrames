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



async def read_payments(
   db: AsyncSession, page: int = 1, limit: int = 10, sort_by: str = None, filter_by: str = None):
    try:
        # Calculate the offset based on the page and limit
        offset = (page - 1) * limit
        # Construct the base query
        query = select(Payment).offset(offset).limit(limit)
        # Apply sorting if provided
        if sort_by:
            if sort_by == "recently-added":
                query = query.order_by(Payment.created_at.desc())
            elif sort_by == "date-asc":
                query = query.order_by(Payment.payment_date.asc())
            elif sort_by == "date-desc":
                query = query.order_by(Payment.payment_date.desc())
            elif sort_by == "amount-asc":
                query = query.order_by(Payment.payment_amount.asc())
            elif sort_by == "amount-desc":
                query = query.order_by(Payment.payment_amount.desc())
            else:
                raise HTTPException(
                    status_code=400, detail="Invalid sort_by parameter"
                )
        else:
                query = query.order_by(Payment.payment_date.desc())
        # Apply filtering if provided
        if filter_by:
            if filter_by == "cash-payment":
                query = query.where(Payment.payment_method == PaymentMethod.CASH)
            elif filter_by == "card-payment":
                query = query.where(Payment.payment_method == PaymentMethod.CARD)
        else:
                query = query.where(Payment.payment_method == PaymentMethod.CASH)
        
        # Execute the query and fetch the results
        result = await db.execute(query)
        payments = result.scalars().all()
        # Calculate the total count of payments
        total_count = await db.scalar(select(func.count()).select_from(Payment))
        # Calculate the total pages
        total_pages = (total_count + limit - 1) // limit
        
        
        payments_list = [
            {
                "payment_id": payment.payment_id,
                "customer_id": payment.customer_id,
                "payment_amount": payment.payment_amount,
                "payment_method": payment.payment_method.value,
                "payment_uid": payment.payment_uid,
                "comments": payment.comments,
                "payment_date": payment.payment_date,
                "created_at": payment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": payment.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for payment in payments
        ]
        return {
            "payments": payments_list,
            "total_pages": total_pages,
            "current_page": page,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
