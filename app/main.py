from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1 import auth, health, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="ThisAbled API", version="0.1.0", lifespan=lifespan)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
