from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Depends

from app.db.session import get_session
from app.services.jwt_controller import JWTController, get_jwt_controller
from app.services.password_controller import PasswordController
from app.utils.utilits import get_user_data_by_username, exception_user_name


class AuthController:
    def __init__(self, jwt_controller: JWTController, session: AsyncSession):
        self.session = session
        self.pass_controller = PasswordController()
        self.jwt_controller = jwt_controller

    async def authenticate_user(self, username: str, password: str):
        # Получение данных о пользователе из user_service
        user_data = await self.get_user_data_by_username(username)

        # Валидация пароля
        is_valid = self.pass_controller.verify_password(password, user_data["hashed_password"], user_data["salt"])
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid password")

        return {"user_data": user_data}

    async def login(self,
                    username: str,
                    password: str):
        # user_data = await self.authenticate_user(username, password)

        # data_for_token = {
        #     "user_name": user_data['user_name'],
        #     "user_id": user_data['user_id'],
        #     # "role":  user.role,
        #     "type": "access"}
        data_for_token = {
            "user_name": 'faiver90',
            "user_id": 56,
            # "role":  user.role,
            "type": "access"}
        access_token = await self.jwt_controller.create_access_token(data_for_token,
                                                                     expires_in=3600)
        data_for_token.update({"type": "refresh"})  # change type for refresh token
        refresh_token = await self.jwt_controller.create_access_token(data_for_token,
                                                                      expires_in=60 * 25)
        return {"access_token": access_token, "refresh_token": refresh_token}


def get_auth_controller(session: AsyncSession = Depends(get_session),
                        jwt_controller: JWTController = Depends(get_jwt_controller)):
    return AuthController(session=session, jwt_controller=jwt_controller)
