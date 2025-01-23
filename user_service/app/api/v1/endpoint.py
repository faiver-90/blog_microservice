from typing import List
from fastapi import Depends, APIRouter

from app.schemas.oauth2_scheme import oauth2_scheme
from app.schemas.users_schemas import CreateUserSchema, UserResponseSchema, UpdateUserSchema, LoginSchema, \
    RefreshTokenSchema
from app.services.users_controller import UserController, get_user_controller

router = APIRouter()


class UserRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route(
            "/add_user/",
            self.add_user,
            methods=["POST"],
            status_code=201,
            tags=["Users"]
        )
        self.router.add_api_route(
            "/get_users/",
            self.get_all_users,
            methods=["GET"],
            response_model=List[UserResponseSchema],
            tags=["Users"]
        )
        self.router.add_api_route(
            "/delete_user/",
            self.delete_user,
            methods=["DELETE"],
            tags=["Users"])
        self.router.add_api_route(
            "/get_current_user/",
            self.get_current_user,
            methods=["GET"],
            response_model=UserResponseSchema,
            tags=["Users"]
        )
        self.router.add_api_route(
            "/update_user/",
            self.update_user,
            methods=["PUT"],
            tags=["Users"])

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme),
                               controller: UserController = Depends(get_user_controller)):
        return await controller.get_current_user_by_token(token)

    @staticmethod
    async def update_user(user_data: UpdateUserSchema,
                          token: str = Depends(oauth2_scheme),
                          controller: UserController = Depends(get_user_controller)):
        return await controller.update_user(user_data, token)

    @staticmethod
    async def add_user(user_data: CreateUserSchema,
                       controller: UserController = Depends(get_user_controller)):
        return await controller.add_user(user_data)

    @staticmethod
    async def get_all_users(controller: UserController = Depends(get_user_controller)):
        return await controller.get_all_users()

    @staticmethod
    async def delete_user(token: str = Depends(oauth2_scheme),
                          controller: UserController = Depends(get_user_controller)):
        return await controller.delete_user(token)
