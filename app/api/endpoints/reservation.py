from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.reservation import reservation_crud
from app.schemas.reservation import ReservationCreate, ReservationDB
from app.api.validators import (check_meeting_room_exists,
                                check_reservation_intersections)

router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(reservation.room_id, session)
    await check_reservation_intersections(
        **reservation.model_dump(
            include=['from_reserve', 'to_reserve', 'room_id']),
        session=session
    )
    new_reservation = await reservation_crud.create(
        reservation,
        session
    )
    return new_reservation
