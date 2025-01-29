from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.users_service import UserService


class UserController:
    def __init__(self, session: AsyncSession):
        self.user_service = UserService(session)

    async def add_user_alt(self, username: str, email: str, password: str):
        try:
            return await self.user_service.add_user(username, email, password)
        except HTTPException as e:
            raise e  # Пропускаем ошибки из репозитория
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {str(e)}")


def get_user_controller(session: AsyncSession = Depends(get_session)):
    return UserController(session)
