# Room Reservation 📅
![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Room Reservation** — это API веб-приложение для бронирования помещений, обеспечивающее эффективное управление и планирование использования комнат.

## Особенности

- **Управление комнатами**: Создание, редактирование и удаление информации о комнатах.
- **Бронирование**: Возможность бронирования комнат с указанием времени начала и окончания.
- **Пользовательская аутентификация**: Регистрация и вход пользователей для управления своими бронированиями.
- **Документация API**: Подробная документация доступна через Swagger UI.

## Установка
Инструкция по локальному запуску

### 1. Клонирование репозитория

```bash
git clone https://github.com/botanikboy/room-reservation.git
cd room-reservation
```

### 2. Установка зависимостей
Убедитесь, что у вас установлен Python 3.9+ и виртуальное окружение.

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
pip install -r requirements.txt
```

### 3. Настройка базы данных
Создайте файл `.env` в корневой директории, указав параметры подключения к вашей базе данных и другие настройки. См. [`.env.example`](https://github.com/botanikboy/room-reservation/blob/main/.env.example) для примера.

Примените миграции для настройки базы данных:

```bash
alembic upgrade head
```

### 4. Запуск приложения
Запустите приложение с помощью Uvicorn:

```bash
uvicorn app.main:reservation_app
```

Приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Основные функции

### 1. Управление комнатами

- Добавление, редактирование и удаление комнат.
- Просмотр списка доступных комнат.

### 2. Бронирование

- Создание бронирований с указанием времени начала и окончания.
- Просмотр своих бронирований.
- Отмена бронирований.

### 3. Пользовательская аутентификация

- Регистрация новых пользователей.
- Вход и выход из системы.

## Технологии

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)

## Будущие планы

- Добавление уведомлений о предстоящих бронированиях.
- Интеграция с календарями (Google Calendar, Outlook).
- Расширение возможностей фильтрации и поиска комнат.
- Возможность интеграции с системами управления зданием.

## Автор

Разработчик: [Ilya Savinkin](https://www.linkedin.com/in/ilya-savinkin-6002a711/)

## Лицензия

Этот проект лицензирован на условиях [MIT License](https://github.com/botanikboy/room-reservation/blob/main/LICENSE).
