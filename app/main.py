from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

reservation_app = FastAPI(title=settings.app_title)

reservation_app.include_router(main_router)
