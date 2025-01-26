from fastapi import APIRouter,Depends,HTTPException,status,Header
from app.schemas.user_schema import Create_Emp,Login_Emp
from app.services import users_service
from app.database.init_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token_schema import Token
from app.core.tokens import verify_token
from app.core.auth import verify_auth_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users",
    tags=["users"],
)



@router.post("/create_emp")
async def create_emp(emp: Create_Emp,db:AsyncSession = Depends(get_db),):
    employee = await users_service.create_emp(emp,db)
    if employee:
        raise HTTPException(status_code=status.HTTP_201_CREATED,detail="Employee created successfully")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Employee not created")
    

@router.post("/login", response_model=Token)
async def login_emp(
    emp: Login_Emp,
    db: AsyncSession = Depends(get_db)
):
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
        
@router.post("/login/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        login_data = Login_Emp(
            emp_id=form_data.username,
            password=form_data.password
        )
        token_data = await users_service.login_emp(login_data, db)
        return token_data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred"
        )


@router.get("/get_employee_name")
async def get_employee_name(
    
    token_data: dict = Depends(verify_auth_token),
    db: AsyncSession = Depends(get_db)
):

    
    
    
    emp_id = token_data.get("emp_id")
    employee = await users_service.get_employee_name(emp_id,db)
    if employee:
        return employee
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found"
    )        
    
    