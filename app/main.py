from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users_route import router as users_router
from app.database.base import base,engine
from app.database.init_db import get_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    print("startup done")
    yield
        




app = FastAPI(
    title="bhatframes backend api",
    description="bhatframes backend api",
    version="0.0.1",
    docs_url="/",
    openapi_url="/openapi.json",
    redoc_url=None,
    lifespan=lifespan
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)