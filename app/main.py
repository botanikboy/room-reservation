from fastapi import FastAPI

from app.api.meeting_room import router
from app.core.config import settings

reservation_app = FastAPI(title=settings.app_title)


@reservation_app.get('/')
def root_get():
    return {'message': 'hello world'}


reservation_app.include_router(router)
