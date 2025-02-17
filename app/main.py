import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.tasks import check_meeting_room_status
from app.core.templates import static_files


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Настройка событий при запуске и завершении приложения."""
#     task = asyncio.create_task(check_meeting_room_status())
#     yield
#     task.cancel()

reservation_app = FastAPI(title=settings.app_title)

reservation_app.include_router(main_router)

reservation_app.mount("/static", static_files, name="static")
