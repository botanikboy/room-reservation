import json
import logging
from fastapi import WebSocket

# Настраиваем логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(
            f"New WebSocket connection established: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
            logger.info(
                f"Sent personal message to {websocket.client}: {message}")
        except Exception as e:
            logger.error(
                f"Error sending personal message to {websocket.client}: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        disconnected_clients = []
        message_json = json.dumps(message)

        logger.info(
            f"Broadcasting message to {len(self.active_connections)} "
            f"clients: {message_json}")

        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
                logger.info(f"Sent message to {connection.client}")
            except Exception as e:
                logger.error(
                    f"Error sending message to {connection.client}: {e}")
                disconnected_clients.append(connection)

        for conn in disconnected_clients:
            self.disconnect(conn)


manager = ConnectionManager()
