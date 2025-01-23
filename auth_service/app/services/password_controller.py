from passlib.context import CryptContext
import secrets


class PasswordController:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def generate_salt(self, salt_length: int = 16) -> str:
        """Генерирует случайную соль."""
        return secrets.token_hex(salt_length)

    def hash_password(self, password: str, salt: str) -> str:
        """Хэширует пароль с использованием соли."""
        salted_password = f"{salt}{password}"
        return self.context.hash(salted_password)

    def verify_password(self, password: str, hashed_password: str, salt: str) -> bool:
        """Проверяет, соответствует ли пароль хэшу."""
        salted_password = f"{salt}{password}"
        return self.context.verify(salted_password, hashed_password)
