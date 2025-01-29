from app.services.users_service import UserService


class UserControllers:
    def __init__(self):
        self.user_service = UserService()