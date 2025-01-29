from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.users_service import UserService


class UserController:
    def __init__(self, session: AsyncSession):
        self.user_service = UserService(session)

    async def add_user(self, username: str, email: str, password: str):
        try:
            return await self.user_service.add_user(username, email, password)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    async def get_all_users(self):
        try:
            return await self.user_service.get_all_users()
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def get_user_controller(session: AsyncSession = Depends(get_session)) -> UserController:
    return UserController(session)
