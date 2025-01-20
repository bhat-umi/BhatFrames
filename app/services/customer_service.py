from datetime import datetime
from app.models.customer_model import Customer,Title
from app.schemas.customer_schema import Create_Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

async def create_customer(request: Create_Customer, db: AsyncSession):
    
    query = select(Customer).where(Customer.customer_contact == request.customer_contact)
    result = await db.execute(query)
    existing_customer = result.scalar_one_or_none()
    
    if existing_customer:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer already exists"
            )
    
    
    new_customer = Customer(
        title=Title(request.title.value),
        customer_first_name=request.customer_first_name,
        customer_last_name=request.customer_last_name,
        customer_address=request.customer_address,
        customer_contact=request.customer_contact,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    try:
        db.add(new_customer)
        await db.commit()
        await db.refresh(new_customer)
        return new_customer
    except Exception as e:
        await db.rollback()
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create custome",
        )