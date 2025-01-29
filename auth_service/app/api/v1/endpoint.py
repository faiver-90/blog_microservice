from fastapi import Depends, APIRouter, HTTPException

from app.schemas.oauth2_scheme import oauth2_scheme
from app.schemas.users_schemas import LoginSchema, RefreshTokenSchema, PasswordValidationSchema, UserCredentialsSchema, \
    TokenSchema
from app.services.jwt_controller import JWTController, get_jwt_controller
from app.services.auth_controller import get_auth_controller, AuthController

router = APIRouter()


class UserRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route(
            "/validate_password/",
            self.validate_password,
            methods=["POST"],
            tags=["Auth"]
        )
        self.router.add_api_route(
            "/create_user_data/",
            self.create_user_data,
            methods=["POST"],
            tags=["Auth"]
        )
        self.router.add_api_route(
            "/refresh_token/",
            self.refresh_token,
            methods=["POST"],
            tags=["Auth"]
        )
        self.router.add_api_route(
            "/token/",
            self.login,
            methods=["POST"],
            tags=["Auth"]
        )
        self.router.add_api_route(
            "/login/",
            self.login,
            methods=["POST"],
            tags=["Auth"]
        )

        self.router.add_api_route(
            "/decode_jwt_token/",
            self.decode_jwt_token,
            methods=["POST"],
            tags=["Auth"]
        )

    @staticmethod
    async def decode_jwt_token(token: str = Depends(oauth2_scheme),
                               auth_controller: AuthController = Depends(get_auth_controller)):
        try:
            print('start decode')
            return await auth_controller.check_jwt_token(token)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def validate_password(user_credentials: PasswordValidationSchema):
        try:
            return {"message": "Пароль прошел проверку"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_user_data(user_credentials: UserCredentialsSchema,
                               auth_controller: AuthController = Depends(get_auth_controller)):
        return await auth_controller.create_user_data(user_credentials)

    @staticmethod
    async def refresh_token(token: RefreshTokenSchema,
                            jwt_controller: JWTController = Depends(get_jwt_controller)):
        return await jwt_controller.refresh_access_token(token.refresh_token)

    @staticmethod
    async def login(user_data: LoginSchema,
                    controller: AuthController = Depends(get_auth_controller)):
        return await controller.login(user_data.username, user_data.password)
