from fastapi import FastAPI

from app.api.meeting_room import router
from app.core.config import settings

reservation_app = FastAPI(title=settings.app_title)

reservation_app.include_router(router)
