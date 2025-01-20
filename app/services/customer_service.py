from datetime import datetime
from app.models.customer_model import Customer, Title
from app.schemas.customer_schema import Create_Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

async def create_customer(request: Create_Customer, db: AsyncSession):
    try:
        # Check for existing customer with the same phone number
        query = select(Customer).where(Customer.customer_contact == request.contact)
        result = await db.execute(query)
        existing_customer = result.scalar_one_or_none()
        
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Customer already exists",
                    "customer_id": existing_customer.customer_id,
                    "customer_name": f"{existing_customer.customer_first_name} {existing_customer.customer_last_name}"
                }
            )
        
        # Create new customer if no duplicate found
        new_customer = Customer(
            title=Title(request.title.value),
            customer_first_name=request.fname,
            customer_last_name=request.lname,
            customer_address=request.address,
            customer_contact=request.contact,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(new_customer)
        await db.commit()
        await db.refresh(new_customer)
        return new_customer

    except HTTPException:
        await db.rollback()
        raise
        
    except Exception as e:
        print(e)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process customer creation"
        )