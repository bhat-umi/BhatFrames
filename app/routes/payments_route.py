from fastapi import APIRouter, Query, Depends, HTTPException, status
from app.core.auth import verify_auth_token
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import payment_service
from app.schemas.payment_schema import PaymentCreate


router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.post("/create")
async def create_payment(
   request:PaymentCreate, token_data: dict = Depends(verify_auth_token), db: AsyncSession = Depends(get_db),
):
    try:
        emp_id = token_data["emp_id"]
        # Create payment in database
        new_payment = await payment_service.create_payment(db, emp_id, request)
       
        if new_payment:
            raise HTTPException(
                status_code=status.HTTP_201_CREATED,
                detail="Payment created successfully",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create payment",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



