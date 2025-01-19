from fastapi import FastAPI
from app.routes.users_route import router as users_router

app = FastAPI(
    title="bhatframes backend api",
    description="bhatframes backend api",
    version="0.0.1",
    docs_url="/",
    openapi_url="/openapi.json",
    redoc_url=None,
    
)


app.include_router(users_router)