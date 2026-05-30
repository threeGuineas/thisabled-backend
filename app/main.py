from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1 import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="ThisAbled API", version="0.1.0", lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
