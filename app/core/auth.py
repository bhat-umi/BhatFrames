from fastapi import Header, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.core.tokens import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login/token", scheme_name="JWT")

async def verify_auth_token(
    authorization: str | None = Header(default=None),
    token: Annotated[str | None, Depends(oauth2_scheme)] = None
) -> dict:
    try:
        # First try header authorization
        if authorization:
            token = authorization.split(" ")[1]
        # If no header, use token from oauth2_scheme
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No valid token provided"
            )
            
        token_data = verify_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return token_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token{}".format(e)
        )