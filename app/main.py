from fastapi import FastAPI

from app.core.config import settings

reservation_app = FastAPI(title=settings.app_title)


@reservation_app.get('/')
def root_get():
    return {'message': 'hello world'}
