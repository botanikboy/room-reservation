import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_async_session
from app.core.websocket_manager import manager
from app.models import Reservation


async def check_meeting_room_status():
    """Фоновая задача для отслеживания статуса переговорок."""
    while True:
        async for session in get_async_session():
            try:
                now = datetime.now()
                query = select(Reservation.room_id).where(
                    Reservation.from_reserve <= now,
                    Reservation.to_reserve >= now
                )
                result = await session.execute(query)
                occupied_rooms = set(result.scalars().all())
                await update_room_status(occupied_rooms)

            except Exception as e:
                print(f"Ошибка в check_meeting_room_status: {e}")

        await asyncio.sleep(15)  # Проверяем статус каждые 15 секунд

current_status = {}


async def update_room_status(occupied_rooms):
    global current_status
    new_status = {room_id: "Occupied" for room_id in occupied_rooms}

    for room_id in current_status.keys():
        if room_id not in occupied_rooms:
            new_status[room_id] = "Free"

    updates = {
        room_id: status for room_id, status in new_status.items()
        if current_status.get(room_id) != status
    }

    if updates:
        for room_id, status in updates.items():
            update_data = {
                "room_id": room_id,
                "status": status
            }
            await manager.broadcast(update_data)

    current_status = new_status
