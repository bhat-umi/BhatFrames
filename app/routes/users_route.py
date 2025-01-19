from fastapi import APIRouter,Depends,HTTPException,status,Header
from app.schemas.user_schema import Create_Emp,Login_Emp
from app.services import users_service
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token_schema import Token
from app.core.tokens import verify_token

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

@router.get("/get_employee_name")
async def get_employee_name(
    
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db)
):

    token = authorization.split(" ")[1]  # Extract token from "Bearer <token>"
    token_data = verify_token(token)
    
    
    emp_id = token_data.get("emp_id")
    employee = await users_service.get_employee_name(emp_id,db)
    if employee:
        return employee
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )        
    
    