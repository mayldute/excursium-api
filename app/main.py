from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.modules.auth.router import router as auth_router
from app.modules.carriers.router import router as carrier_router
from app.modules.clients.router import router as client_router
from app.modules.transports.router import router as transport_router
from app.tasks.cleanup import (
    delete_deleted_users,
    delete_oauth_state,
    delete_unactivated_users,
    delete_unchanged_emails,
)


def build_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_oauth_state, "interval", minutes=10)
    scheduler.add_job(delete_unchanged_emails, "interval", minutes=30)
    scheduler.add_job(delete_unactivated_users, "interval", hours=1)
    scheduler.add_job(delete_deleted_users, "interval", days=1)
    return scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    scheduler = build_scheduler()
    scheduler.start()
    app.state.scheduler = scheduler

    try:
        yield
    finally:
        scheduler.shutdown(wait=False)


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app.app_name,
        version="2.0.0",
        debug=settings.app.debug,
        lifespan=lifespan,
    )

    application.include_router(auth_router, prefix="/api/v1")
    application.include_router(client_router, prefix="/api/v1")
    application.include_router(carrier_router, prefix="/api/v1")
    application.include_router(transport_router, prefix="/api/v1")

    register_exception_handlers(application)

    @application.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_application()
