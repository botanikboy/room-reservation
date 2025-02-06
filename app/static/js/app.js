let ganttChart; // Глобальная переменная для диаграммы
let reservations = []; // Глобальная переменная для хранения бронирований

document.addEventListener("DOMContentLoaded", () => {
    reservations = [{"from_reserve": "2025-02-06T16:31:00", "id": 6, "room_id": 1, "to_reserve": "2025-02-06T17:21:00"}];
    renderGanttChart(reservations);

    // Подключение WebSocket
    const ws = new WebSocket("ws://localhost:8000/ws/meeting_rooms");

    ws.onmessage = (event) => {
        try {
            const newReservation = JSON.parse(event.data);
            if (newReservation.from_reserve && newReservation.to_reserve && newReservation.room_name) {
                reservations.push(newReservation); // Добавляем новое бронирование в глобальный список
                updateGanttChart(newReservation);
            } else {
                console.error("Invalid reservation data:", event.data);
            }
        } catch (e) {
            console.error("Error parsing WebSocket message:", e);
        }
    };
});

function renderGanttChart(reservations) {
    const ctx = document.getElementById("ganttChart").getContext("2d");

    // Уничтожаем предыдущую диаграмму, если она существует
    if (ganttChart) {
        ganttChart.destroy();
    }

    const datasets = reservations.map(res => ({
        label: res.room_name,
        data: [{
            x: [new Date(res.from_reserve), new Date(res.to_reserve)],
            y: res.room_name
        }],
        backgroundColor: "rgba(75, 192, 192, 0.5)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1
    }));

    ganttChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: reservations.map(res => res.room_name),
            datasets: datasets
        },
        options: {
            indexAxis: "y",
            scales: {
                x: {
                    type: "time",
                    time: {
                        unit: "hour",
                        tooltipFormat: "HH:mm",
                        displayFormats: { hour: "HH:mm" }
                    },
                    min: new Date().setHours(6, 0, 0, 0),
                    max: new Date().setHours(23, 59, 59, 999)
                }
            }
        }
    });
}


function updateGanttChart(newReservation) {
    const existingIndex = ganttChart.data.datasets.findIndex(d => d.label === newReservation.room_name);

    if (existingIndex !== -1) {
        ganttChart.data.datasets[existingIndex].data = [{
            x: [new Date(newReservation.from_reserve), new Date(newReservation.to_reserve)],
            y: newReservation.room_name
        }];
    } else {
        ganttChart.data.datasets.push({
            label: newReservation.room_name,
            data: [{
                x: [new Date(newReservation.from_reserve), new Date(newReservation.to_reserve)],
                y: newReservation.room_name
            }],
            backgroundColor: "rgba(75, 192, 192, 0.5)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1
        });
    }

    ganttChart.update();
}
