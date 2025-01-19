from pydantic import BaseModel,field_validator
from enum import Enum

class Role(str,Enum):
    admin = "admin"
    employee = "employee"




class Create_Emp(BaseModel):
    emp_id:str
    emp_name:str
    password:str
    role:Role
    
    @field_validator("role")
    def validate_role(cls,value):
        if value not in Role:
            raise ValueError("Invalid role")
        return value


class Login_Emp(BaseModel):
    emp_id:str
    password:str

