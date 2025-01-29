from typing import List

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import User


class UserRepository:
    """Репозиторий для работы с пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, username: str, email: str):
        """Create user"""
        try:
            user = User(username=username, email=email)
            self.session.add(user)
            await self.session.commit()
            return user
        except IntegrityError as e:
            await self.session.rollback()
            error_message = str(e.orig)
            if "user_account_username_key" in error_message:
                raise HTTPException(status_code=400, detail="Пользователь с таким username уже существует")
            elif "user_account_email_key" in error_message:
                raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
            else:
                raise HTTPException(status_code=400, detail="Ошибка уникальности данных")
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {str(e)}")


    async def delete_user(self, user_id: int):
        """Delete user"""
        try:
            query = delete(User).where(User.id == user_id)
            await self.session.execute(query)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    async def get_all_users(self) -> List[User]:
        """Get all users from DB"""
        try:
            stmt = select(User).options(selectinload(User.userprofile))
            result = await self.session.execute(stmt)

            # Сохраняем результат в переменную, чтобы избежать двойного вызова
            users = result.scalars().all()

            if not users:  # Проверяем список сразу
                raise HTTPException(status_code=404, detail="Users not found")

            return users
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    async def get_user_by_username(self, username: str) -> User:
        """Get one user from DB by username"""
        try:
            stmt = select(User).options(selectinload(User.userprofile)).where(User.username == username)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
