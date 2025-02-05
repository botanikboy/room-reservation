import json
import random
import asyncio
from fastapi import WebSocket, APIRouter, WebSocketDisconnect

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
async def websocket_rooms(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            room_status = random.choice(["occupied", "free"])
            data = {
                "room_id": 1,
                "room_name": "Room A",
                "status": room_status
            }
            await manager.broadcast(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
