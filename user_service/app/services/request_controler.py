import httpx
from fastapi import HTTPException


class RequestController:
    """Базовый контроллер с универсальным обработчиком запросов."""

    @staticmethod
    async def execute_request(method: str, url: str, json_data: dict = None):
        """Универсальный метод для выполнения HTTP-запросов."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=json_data)

            if response.status_code not in {200, 201}:
                error_detail = response.json().get("detail", "Unknown error")
                raise HTTPException(status_code=response.status_code, detail=error_detail)

            return response.json()

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка сети: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
