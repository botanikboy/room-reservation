document.addEventListener("DOMContentLoaded", () => {
    const ws = new WebSocket("ws://localhost:8000/ws/meeting_rooms");

    ws.onmessage = (event) => {
        const logContainer = document.getElementById("log");
        const data = JSON.parse(event.data);

        // Обновление статуса комнаты
        const roomStatus = document.getElementById(`status-${data.room_id}`);
        if (roomStatus) {
            roomStatus.textContent = "Occupied";
            roomStatus.classList.remove("bg-secondary", "bg-success");
            roomStatus.classList.add("bg-danger");
        }

        // Логирование сообщения
        const logEntry = document.createElement("div");
        logEntry.innerHTML = `
            <a href="#" class="text-primary fw-bold">${data.user_name}</a> 
            ${data.action} reservation: 
            <strong>Room ${data.room_id}</strong>, 
            From: ${data.from_reserve}, 
            To: ${data.to_reserve}
        `;

        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    };
});
