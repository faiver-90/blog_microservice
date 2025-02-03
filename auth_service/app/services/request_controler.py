import httpx
from fastapi import HTTPException


class RequestController:
    """Базовый контроллер с универсальным обработчиком запросов."""

    @staticmethod
    async def execute_request(method: str, url: str, json_data=None, headers=None):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=json_data, headers=headers)

        if response.status_code == 200:
            return response.json()  # Успешный ответ

        try:
            error_data = response.json()  # Парсим JSON-ошибку
        except ValueError:  # Если тело ответа пустое или не JSON
            error_data = {"detail": "Unknown error from external service"}

        raise HTTPException(status_code=response.status_code, detail=error_data.get("detail", "Unknown error"))


def get_request_controller():
    return RequestController()
