# 📚 FastAPI Auth и User Management Микросервисы

Этот проект демонстрирует реализацию микросервисов для **аутентификации** и **управления пользователями** с использованием **FastAPI**. Он подходит для изучения микросервисной архитектуры, REST API и токенной авторизации (JWT).

---

## 📦 Функциональность

### 🔐 Auth Service (`http://localhost:8001`)
| Метод | URL                        | Назначение                          |
|--------|----------------------------|-------------------------------------|
| POST   | `/validate_password/`     | Проверка пароля                     |
| POST   | `/create_user_data/`      | Создание пользователя               |
| POST   | `/refresh_token/`         | Обновление токена                   |
| POST   | `/token/`                 | Аутентификация и выдача токена      |
| POST   | `/login/`                 | Авторизация                         |
| POST   | `/decode_jwt_token/`      | Расшифровка JWT токена              |

### 📅 User Service (`http://localhost:8002/user`)
| Метод  | URL                                   | Назначение                             |
|--------|----------------------------------------|----------------------------------------|
| GET    | `/get_users/`                         | Получение списка всех пользователей    |
| GET    | `/get_current_user/`                  | Информация о текущем пользователе      |
| GET    | `/get_user_id_by_username/`           | Получение ID пользователя по username  |
| POST   | `/add_user/`                          | Добавление нового пользователя         |
| PUT    | `/update_user/`                       | Обновление данных пользователя         |
| DELETE | `/delete_user/`                       | Удаление пользователя по токену        |

Swagger UI доступен по:
- `http://localhost:8001/docs` (auth)
- `http://localhost:8002/docs` (user)

---

## 🛠️ Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/faiver-90/blog_microservice.git .
```

### 2. Установите зависимости
```bash
# Виртуальное окружение
python -m venv env
source env/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows

# Установка
pip install -r requirements.txt
```

### 3. Создай файлы `.env` в `auth_service` и `user_service`
Пример содержимого:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=user
DB_USER=user
DB_PASSWORD=user
JWT_SECRET_KEY=secret
```

### 4. Запуск сервисов вручную
```bash
uvicorn auth_service.app.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn user_service.app.main:app --host 0.0.0.0 --port 8002 --reload
```

### 5. Или запуск через Docker Compose
```bash
docker-compose up --build
```

---

## 🔗 Примеры запросов (Postman)

### 🔑 POST `/user/add_user/`
```json
{
  "username": "new_user",
  "email": "new_user@example.com",
  "password": "secure_password"
}
```

### 🔓 POST `/auth/token/`
```json
{
  "username": "new_user",
  "password": "secure_password"
}
```

### 🔒 GET `/user/get_current_user/`
**Headers:**
```
Authorization: Bearer <JWT Token>
```

---

## 📙 Технологии
- **FastAPI** — REST API
- **Pydantic** — валидация данных
- **JWT** — авторизация
- **Docker / Compose** — контейнеризация
- **PostgreSQL** — база данных

---

## 🧪 Тесты
```bash
pytest
```

