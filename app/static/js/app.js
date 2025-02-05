// static/js/app.js

// Подключение к WebSocket-серверу
const ws = new WebSocket("ws://localhost:8000/ws/meeting_rooms");

// Ссылка на элемент списка
const roomsList = document.getElementById("rooms-list");

// При подключении WebSocket
ws.onopen = () => {
    console.log("WebSocket connected");
};

// При получении сообщений
ws.onmessage = (event) => {
    const data = JSON.parse(event.data); // Парсим JSON
    console.log("Received:", data);
    updateRoomStatus(data); // Обновляем интерфейс
};

// Обновление списка переговорных
function updateRoomStatus(room) {
    // Ищем элемент списка для текущей комнаты
    let roomElement = document.getElementById(`room-${room.room_id}`);

    if (!roomElement) {
        // Если комната не существует, создаём новый элемент
        roomElement = document.createElement("li");
        roomElement.id = `room-${room.room_id}`;
        roomElement.classList.add("list-group-item", "d-flex", "justify-content-between");
        roomsList.appendChild(roomElement);
    }

    // Обновляем текст и статус комнаты
    roomElement.textContent = `${room.room_name}`;
    roomElement.classList.remove("list-group-item-success", "list-group-item-danger");
    roomElement.classList.add(room.status === "occupied" ? "list-group-item-danger" : "list-group-item-success");
    roomElement.textContent += room.status === "occupied" ? " (Occupied)" : " (Free)";
}
