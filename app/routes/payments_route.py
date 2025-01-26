from fastapi import APIRouter, Query, Depends, HTTPException, status
from app.core.auth import verify_auth_token
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import payment_service
from app.schemas.payment_schema import PaymentCreate
from enum import Enum
from app.core.auth import verify_auth_token
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payment_model import Payment, PaymentMethod
from fastapi.responses import JSONResponse




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


class SortOptions(str, Enum):
    DATE_ASC = "date-asc"
    DATE_DESC = "date-desc"
    AMOUNT_ASC = "amount-asc"
    AMOUNT_DESC = "amount-desc"
class FilterOptions(str, Enum):
    CASH_PAYMENT = "cash-payment"
    CARD_PAYMENT = "card-payment"

@router.get("/read")
async def read_payments(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=10, gt=0),
    sort_by: SortOptions = Query(default="date-asc"),
    filter_by: FilterOptions = Query(default="cash-payment"),
    token_data: dict = Depends(verify_auth_token),
   
):
    try:
        payments = await payment_service.read_payments(
            db,
            page,
            limit,
            sort_by=sort_by.value if sort_by else None,
            filter_by=filter_by.value,
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=payments)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":"{}".format(e)},
        )
