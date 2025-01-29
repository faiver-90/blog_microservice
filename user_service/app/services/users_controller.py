import asyncio
from typing import List

import httpx
from sqlalchemy import delete, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Depends

from app.db.models import User, UserProfile
from app.db.session import get_session
from app.utils.utilits import get_user_by_username, get_all_users, get_payload_from_token, exception_id, \
    exception_user_name

from app.schemas.users_schemas import CreateUserSchema, UserResponseSchema, UserProfileSchema


class UserController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_user(self,
                          user_data,
                          token: dict):
        payload = await get_payload_from_token(token)
        user_name = payload.get("user_name")
        user = await get_user_by_username(user_name, self.session)

        await exception_user_name(user_name)

        user_attributes = {attr.key for attr in inspect(User).mapper.column_attrs}
        profile_attributes = {attr.key for attr in inspect(UserProfile).mapper.column_attrs}

        user_data_dict = user_data.dict(exclude_unset=True)  # Исключаем поля, которые не были переданы

        for field, value in user_data_dict.items():
            if field in user_attributes:  # Если поле относится к User
                setattr(user, field, value)
            elif field in profile_attributes:  # Если поле относится к UserProfile
                if user.userprofile:
                    setattr(user.userprofile, field, value)
                else:
                    # Создаём профиль, если его нет
                    user.userprofile = UserProfile(**{field: value})

        # Сохранение изменений
        await self.session.commit()

        return {"message": "Updated"}

    async def validate_password(self, password: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://auth_service:8000/auth/validate_password/",
                                         json={"password": password})
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail=response.json().get("detail"))

    async def create_user(self, user_data: CreateUserSchema):
        print(f"📥 Полученные данные: {user_data.dict()}")  # Логируем данные

        try:
            user = User(
                username=user_data.username,
                fullname=user_data.full_name,
                userprofile=UserProfile(work=user_data.work),
                email=user_data.email
            )
            self.session.add(user)
            await self.session.commit()
            return {"message": "User added successfully", 'user_id': user.id}
        except IntegrityError as e:
            await self.session.rollback()
            error_message = str(e.orig)
            if "user_account_username_key" in error_message:
                raise HTTPException(status_code=400,
                                    detail="Username already exists. Please choose a different username.")
            elif "user_account_email_key" in error_message:
                raise HTTPException(status_code=400,
                                    detail="Email already exists. Please use a different email address.")
            else:
                raise HTTPException(status_code=400,
                                    detail="A database integrity error occurred. Please check your data.")

    async def create_auth_record(self, user_id: int, password: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://auth_service:8000/auth/create_user_data/",
                    json={"user_id": user_id, "password": password}
                )
                print('response.status_code', response.status_code)

        except Exception as e:
            raise HTTPException(status_code=501, detail=f"Ошибка при отправке запроса: {e}")

    async def add_user(self, user_data: CreateUserSchema):
        """Добавление пользователя с валидацией пароля"""
        await self.validate_password(user_data.password)
        user_data_dict = await self.create_user(user_data)
        user_id = int(user_data_dict['user_id'])
        user_check = await self.session.get(User, user_id)
        print(user_check)
        await self.create_auth_record(user_id, user_data.password)

        query = delete(User).where(User.id == user_id)
        await self.session.execute(query)
        await self.session.commit()

        return {"message": "Пользователь создан"}

    async def get_all_users(self) -> List[UserResponseSchema]:
        users = await get_all_users(self.session)
        if not users:
            raise HTTPException(status_code=404, detail="User not found")

        # Преобразование в схемы
        return [
            UserResponseSchema(
                username=user.username,
                full_name=user.fullname,
                key=user.key,
                profile=UserProfileSchema.model_validate(user.userprofile) if user.userprofile else None
            )
            for user in users
        ]

    async def get_current_user_by_token(self,
                                        token: dict) -> UserResponseSchema:
        payload = await get_payload_from_token(token)

        user = await get_user_by_username(payload.get('user_name'), self.session)
        await exception_id(payload.get('user_id'))
        await exception_user_name(payload.get('user_name'))
        user_schema = UserResponseSchema(
            username=user.username,
            key=user.key,
            profile=UserProfileSchema.model_validate(user.userprofile) if user.userprofile else None
        )

        return user_schema

    async def delete_user(self,
                          token: dict):
        payload = await get_payload_from_token(token)
        user_id = payload.get('user_id')

        await exception_id(payload.get('user_id'))

        user_name = payload.get('user_name')

        await exception_user_name(user_name)

        query = delete(User).where(User.id == user_id)
        await self.session.execute(query)
        await self.session.commit()
        return {"message": f"Deleted user: {user_name}"}


def get_user_controller(session: AsyncSession = Depends(get_session)):
    return UserController(session=session)


async def main():
    uses_service = get_user_controller()
    await uses_service.add_user(
        {
            "salt": "string",
            "password": "st$Rr7877ing",
            "user_id": "2"
        }
    )


if __name__ == '__main__':
    asyncio.run(main())
