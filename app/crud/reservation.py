from datetime import datetime, time
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(
            self,
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            room_id: int,
            reservation_id: Optional[int] = None,
            session: AsyncSession) -> list[Reservation]:
        select_stmt = select(Reservation).where(
                Reservation.room_id == room_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve
                )
        )
        if reservation_id is not None:
            select_stmt = select_stmt.where(Reservation.id != reservation_id)
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.room_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        return reservations.scalars().all()

    async def get_by_user(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> list[Reservation]:
        reservations = await session.execute(
            select(Reservation).where(Reservation.user_id == user_id)
        )
        return reservations.scalars().all()

    async def get_today_reservations(
            self,
            session: AsyncSession
    ) -> list[Reservation]:
        today = datetime.now().date()
        start_of_day = datetime.combine(today, time(6, 0, 0))
        end_of_day = datetime.combine(today, time(23, 59, 59))

        query = select(Reservation).where(
            Reservation.from_reserve >= start_of_day,
            Reservation.from_reserve <= end_of_day
        )
        result = await session.execute(query)
        return result.scalars().all()


reservation_crud = CRUDReservation(Reservation)
