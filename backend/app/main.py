import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.api.router import api_router
from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import register_exception_handlers
from app.core.framework.models import PublicContent as _public_content_model

logging.getLogger("slow_queries").setLevel(logging.WARNING)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        if duration > 0.5:
            print(
                f"SLOW REQUEST: {request.method} {request.url.path} "
                f"took {duration * 1000:.0f}ms"
            )
        return response


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Public Content", "description": "Public records and editorial content."},
        {"name": "System", "description": "Staff authentication and setup."},
    ],
)

register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With"],
    expose_headers=["Content-Disposition"],
)
app.add_middleware(TimingMiddleware)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    from sqlalchemy import text
    from app.core.database import async_session_maker

    try:
        async with async_session_maker() as session:
            row = await session.execute(text("SELECT version()"))
            return {
                "status": "healthy",
                "database": {"connected": True, "version": row.scalar()},
            }
    except Exception as exc:
        return {
            "status": "degraded",
            "database": {"connected": False, "version": str(exc)},
        }


fastapi_app = app
