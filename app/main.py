from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.templates import static_files

reservation_app = FastAPI(title=settings.app_title)

reservation_app.include_router(main_router)

reservation_app.mount("/static", static_files, name="static")
