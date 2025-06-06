import bcrypt
from passlib.context import CryptContext
import secrets


class PasswordController:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate_salt(self, salt_length: int = 16) -> str:
        """Генерирует случайную соль."""
        return bcrypt.gensalt(salt_length)

    def hash_password(self, password: str, salt) -> str:
        """Хэширует пароль с использованием bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет соответствие пароля хэшу."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_pass_controller():
    return PasswordController()
