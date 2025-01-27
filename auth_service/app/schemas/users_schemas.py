import uuid

from pydantic import BaseModel, Field, field_validator


class LoginSchema(BaseModel):
    username: str
    password: str = Field(default='Stri54_ng')


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class UserCredentialsSchema(BaseModel):
    salt: str
    password: str
    user_id: int

    model_config = {
        "from_attributes": True
    }

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char in "!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/" for char in value):
            raise ValueError("Password must contain at least one special character")
        return value
