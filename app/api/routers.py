from fastapi import APIRouter

from app.api.endpoints import reservation_router, room_router

main_router = APIRouter()
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)
main_router.include_router(
    room_router, prefix='/meeting_rooms', tags=['Meeting Rooms']
)
