from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.user_schema import Create_Emp,Login_Emp
from app.services import users_service
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token_schema import Token
router = APIRouter(
    prefix="/users",
    tags=["users"],
)



@router.post("/create_emp")
async def create_emp(emp: Create_Emp,db:AsyncSession = Depends(get_db)):
    employee = await users_service.create_emp(emp,db)
    if employee:
        raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Employee created successfully")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Employee not created")
    

@router.post("/login", response_model=Token)
async def login_emp(emp: Login_Emp, db: AsyncSession = Depends(get_db)):
    try:
        token_data = await users_service.login_emp(emp, db)
        return token_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred"
        )