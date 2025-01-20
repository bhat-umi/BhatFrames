from datetime import datetime
from app.models.customer_model import Customer, Title
from app.schemas.customer_schema import Create_Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status


async def create_customer(request: Create_Customer, db: AsyncSession):
    try:
        query = select(Customer).where(
            Customer.customer_contact == request.contact
        )
        
        result = await db.execute(query)
        print("result is ", result)
        existing_customer = result.scalars().all()
        
        print("existing_customer is ", existing_customer)
        if len(existing_customer) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer with this contact number already exists",
            )

        new_customer = Customer(
            title=Title(request.title.value),
            customer_first_name=request.fname,
            customer_last_name=request.lname,
            customer_address=request.address,
            customer_contact=request.contact,
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
