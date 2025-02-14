from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.websocket_manager import manager

router = APIRouter()


@router.websocket('/meeting_rooms')
async def websocket_rooms(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_async_session)
):
    await manager.connect(websocket)
    await websocket.send_text("WebSocket connected")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
