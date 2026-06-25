from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1 import auth, health, posts, stt, upload, users, vision
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="ThisAbled API", version="0.1.0", lifespan=lifespan)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(vision.router, prefix="/api/v1")
app.include_router(stt.router, prefix="/api/v1")
