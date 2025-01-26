from fastapi import APIRouter, Depends, Header, HTTPException, status,Query
from fastapi.responses import JSONResponse
from app.schemas.customer_schema import Create_Customer
from app.services import customer_service
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.tokens import verify_token
from app.core.auth import verify_auth_token

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post("/create")
async def create_customer(
    request: Create_Customer,

    db: AsyncSession = Depends(get_db),
    token_data: dict = Depends(verify_auth_token),
):
    try:
        
        if not token_data:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Invalid token"}
            )
        

        customer = await customer_service.create_customer(request, db)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Customer created successfully",
                "data": {
                    "customer_id": customer.customer_id,
                    "customer_name": f"{customer.customer_first_name} {customer.customer_last_name}"
                }
            }
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.detail}
        )
        
    except Exception as e:
        print("error", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error occurred"}
        )

from enum import Enum
from fastapi import Query

class SortOptions(str, Enum):
    AZ = "name-asc"
    ZA = "name-desc"
    BALANCE_LOW_HIGH = "balance-high"
    BALANCE_HIGH_LOW = "balance-low"
    RECENTLY_ADDED = "recently-added"

class FilterOptions(str, Enum):
    ALL = "all"
    WITH_BALANCE = "with_balance"

@router.get("/read")
async def read_customers(
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=10, gt=0),
    sort_by: SortOptions = Query(default='recently-added'),
    filter_by: FilterOptions = Query(default="all"),
    token_data: dict = Depends(verify_auth_token),
    db: AsyncSession = Depends(get_db)
):
    try:
        customers = await customer_service.read_customers(
            db, 
            page, 
            limit, 
            sort_by=sort_by.value if sort_by else None,
            filter_by=filter_by.value
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=customers
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error occurred"}
        )        
        
@router.get("/search")
async def search_customers(
    token_data: dict = Depends(verify_auth_token),
    search_query: str = Query(..., min_length=3),
    db: AsyncSession = Depends(get_db)):
    try:
        customers = await customer_service.search_customers(db, search_query)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=customers
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        print("error", e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error occurred"},
        )
