import asyncio

import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException

from app.db.models import UserCredentials
from app.db.session import get_session
from app.schemas.users_schemas import PasswordValidationSchema, RefreshTokenSchema, TokenSchema
from app.services.jwt_controller import JWTController, get_jwt_controller, JWT_SECRET_KEY, JWT_ALGORITHM
from app.services.password_controller import PasswordController


class AuthController:
    def __init__(self, jwt_controller: JWTController, session: AsyncSession):
        self.session = session
        self.pass_controller = PasswordController()
        self.jwt_controller = jwt_controller

    async def check_jwt_token(self, token):
        try:
            payload = await self.jwt_controller.decode_access_token(token)
            if payload.get("type") != "access":
                raise HTTPException(status_code=403, detail="Invalid token type")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def validate_password(self, payload: PasswordValidationSchema):
        try:
            return {"message": "Пароль прошел проверку"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def create_user_data(self, user_credentials):
        try:
            salt = self.pass_controller.generate_salt()
            hashed_password = self.pass_controller.hash_password(user_credentials.password, salt)

            user_data = UserCredentials(
                salt=str(salt),
                hashed_password=hashed_password,
                user_id=user_credentials.user_id
            )
            self.session.add(user_data)
            await self.session.commit()
            return {'message': 'complete'}

        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="User ID already exists")

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

    async def authenticate_user(self, username: str, password: str):
        # Получение данных о пользователе из user_service
        # user_data = await self.get_user_data_by_username(username)
        #
        # # Валидация пароля
        # is_valid = self.pass_controller.verify_password(password, user_data["hashed_password"], user_data["salt"])
        # if not is_valid:
        #     raise HTTPException(status_code=401, detail="Invalid password")
        #
        # return {"user_data": user_data}
        print(username, password)

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
            "user_name": 'faiver9023',
            "user_id": 97,
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

    # async def run():
    #     auth = get_auth_controller()
    #     await auth.authenticate_user('asda', 'jhkh')
    #
    # if __name__ == "__main__":
    #     asyncio.run(run())
