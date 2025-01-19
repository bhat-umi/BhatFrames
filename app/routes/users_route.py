from fastapi import APIRouter
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/users")
async def get_users():
    return {"message": "Hello World"}


