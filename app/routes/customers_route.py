from fastapi import APIRouter,  Depends , Header, HTTPException, status
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
async def create_customer(request: Create_Customer,authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    print(request.title.value)
    token = authorization.split(" ")[1]  
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    customer = await customer_service.create_customer(request, db)
    return True
