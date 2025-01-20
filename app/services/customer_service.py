from datetime import datetime
from app.models.customer_model import Customer, Title
from app.schemas.customer_schema import Create_Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status


async def create_customer(request: Create_Customer, db: AsyncSession):
    try:
        query = select(Customer).where(
            Customer.customer_contact == request.customer_contact
        )
        result = await db.execute(query)
        existing_customer = result.scalar_one_or_none()

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer with this contact number already exists",
            )

        new_customer = Customer(
            title=Title(request.title.value),
            customer_first_name=request.customer_first_name,
            customer_last_name=request.customer_last_name,
            customer_address=request.customer_address,
            customer_contact=request.customer_contact,
            balance=request.balance,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(new_customer)
        await db.commit()
        await db.refresh(new_customer)
        return new_customer

    except HTTPException:
        await db.rollback()
        
    except Exception as e:
        print(f"Error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create customer. Please try again later.",
        )
