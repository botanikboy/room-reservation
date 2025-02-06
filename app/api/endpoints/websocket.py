import json
import random
import asyncio

from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.core.db import get_async_session

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except RuntimeError:
                disconnected_clients.append(connection)
        for conn in disconnected_clients:
            self.disconnect(conn)


manager = ConnectionManager()


@router.websocket('/meeting_rooms')
async def websocket_rooms(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_async_session)
):
    await manager.connect(websocket)
    try:
        room_ids = await meeting_room_crud.get_multi(session)
        # while True:
        #     for room_id in room_ids:
        #         room_status = random.choice(["occupied", "free"])
        #         data = {
        #             "room_id": room_id.id,
        #             "status": room_status
        #         }
        #         await manager.broadcast(data)
        #         await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
