from datetime import datetime
from app.models.customer_model import Customer, Title
from app.schemas.customer_schema import Create_Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status
import math

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
        print("Request:",request.model_dump())
        new_customer = Customer(
            title=Title(request.title.value),
            customer_first_name=request.fname,
            customer_last_name=request.lname,
            customer_address=request.address,
            customer_contact=request.contact,
            balance=request.balance,
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


async def read_customers(db: AsyncSession, page: int = 1, limit: int = 10):
    try:
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get total count
        count_query = select(func.count()).select_from(Customer)
        total_count = await db.scalar(count_query)
        
        # Get paginated customers
        query = select(Customer).order_by(Customer.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        customers = result.scalars().all()
        
        if not customers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No customers found"
            )
            
        customers_list = [
            {
                "customer_id": customer.customer_id,
                "title": customer.title.value,
                "customer_first_name": customer.customer_first_name,
                "customer_last_name": customer.customer_last_name,
                "customer_address": customer.customer_address,
                "balance": customer.balance,
                "customer_contact": customer.customer_contact,
                "created_at": customer.created_at.isoformat(),
                "updated_at": customer.updated_at.isoformat()
            }
            for customer in customers
        ]
        
        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total_count / limit),
            "data": customers_list
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch customers"
        )


async def search_customers(db: AsyncSession, query: str, page: int = 1, limit: int = 10):
    try:
        # Calculate offset
        offset = (page - 1) * limit

        # Get total count
        count_query = select(func.count()).select_from(Customer).where(
            (Customer.customer_first_name.ilike(f"%{query}%")) |
            (Customer.customer_last_name.ilike(f"%{query}%")) |
            (Customer.customer_contact.ilike(f"%{query}%"))
        )
        total_count = await db.scalar(count_query)

        # Get paginated customers
        query = select(Customer).where(
            (Customer.customer_first_name.ilike(f"%{query}%")) |
            (Customer.customer_last_name.ilike(f"%{query}%")) |
            (Customer.customer_contact.ilike(f"%{query}%"))
        ).order_by(Customer.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        customers = result.scalars().all()
        if not customers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No customers found"
            )

        customers_list = [
            {
                "customer_id": customer.customer_id,
                "title": customer.title.value,
                "customer_first_name": customer.customer_first_name,
                "customer_last_name": customer.customer_last_name,
                "customer_address": customer.customer_address,
                "customer_contact": customer.customer_contact,
                "balance": customer.balance,
                "created_at": customer.created_at.isoformat(),
                "updated_at": customer.updated_at.isoformat()
            }
            for customer in customers
        ]

        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total_count / limit),
            "data": customers_list
        }

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No customers found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch customers",
        )
