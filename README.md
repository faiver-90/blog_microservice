# 📚 FastAPI Auth and User Management Service

Этот проект демонстрирует реализацию базовой аутентификации и управления пользователями с использованием FastAPI. Проект ориентирован на изучение и демонстрацию навыков работы с микросервисной архитектурой, API и FastAPI.

## 📦 Возможности

### Auth Service
- **POST /validate_password/**: Проверка пароля на соответствие требованиям.
- **POST /create_user_data/**: Создание пользователя.
- **POST /refresh_token/**: Обновление токена доступа.
- **POST /token/**: Аутентификация пользователя и получение токена.
- **POST /login/**: Авторизация пользователя.
- **POST /decode_jwt_token/**: Расшифровка JWT токена.

### User Service
- **GET /get_users/**: Получение списка всех пользователей.
- **GET /get_current_user/**: Получение информации о текущем пользователе по токену.
- **GET /get_user_id_by_username/**: Получение ID пользователя по имени.
- **POST /add_user/**: Добавление нового пользователя.
- **PUT /update_user/**: Обновление данных пользователя.
- **DELETE /delete_user/**: Удаление пользователя.

## 🛠️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/faiver-90/blog_microservice.git .
```

### 2. Установка зависимостей
Создайте .env файлы в сервисах.
```bash
# Установите виртуальное окружение
python -m venv env
source env/bin/activate  # для Linux/MacOS
venv\Scripts\activate  # для Windows

# Установите зависимости
pip install -r requirements.txt
```

### 3. Запуск сервера

#### Auth Service
```bash
uvicorn auth_service.app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### User Service
```bash
uvicorn user_service.app.main:app --host 0.0.0.0 --port 8002 --reload
```

### 4. Запуск через Docker Compose

Если установлен Docker и Docker Compose, просто выполните:
```bash
docker-compose up --build
```

## 🔗 Примеры запросов

### Аутентификация
**POST /auth_service/token/**
```json
{
  "username": "example_user",
  "password": "example_password"
}
```

### Создание пользователя
**POST /user_service/add_user/**
```json
{
  "username": "new_user",
  "email": "new_user@example.com",
  "password": "secure_password"
}
```

## 📚 Технологии
- **FastAPI** для создания RESTful API
- **Pydantic** для валидации данных
- **JWT** для аутентификации
- **Docker** для контейнеризации
- **PostgreSQL**

## 🧪 Тестирование
Для запуска тестов выполните:
```bash
pytest
```

