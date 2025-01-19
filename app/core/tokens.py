import jwt 
from datetime import datetime, timedelta
from app.core.config import settings


print(settings.SECRET_KEY)
print(settings.ALGORITHM)
print(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(emp_id:str, role: str):
    
    payload = {
        "emp_id": emp_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    encoded_jwt =  jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(emp_id:str,role:str):

    payload = {
        "emp_id": emp_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    