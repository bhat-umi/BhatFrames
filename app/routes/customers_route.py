from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.customer_schema import Create_Customer
from app.services import customer_service
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.tokens import verify_token


router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post("/create")
async def create_customer(
    request: Create_Customer,
    authorization: str = Header(...), 
    db: AsyncSession = Depends(get_db)
):
    try:
        token = authorization.split(" ")[1]
        token_data = verify_token(token)
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
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error occurred"}
        )
