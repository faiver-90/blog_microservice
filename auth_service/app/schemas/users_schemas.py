import uuid

from pydantic import BaseModel, Field, EmailStr, field_validator


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=5, default='Vladimir')
    full_name: str | None = Field(default='Malashkin')
    email: EmailStr | None = None
    password: str = Field(min_length=8, default='Stri54_ng')
    work: str | None = Field(default='Web-developer')

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


class UserProfileSchema(BaseModel):
    work: str | None = None

    model_config = {
        "from_attributes": True,
    }


class UserResponseSchema(BaseModel):
    username: str = Field(...)
    full_name: str | None = None
    key: uuid.UUID | None = None
    profile: UserProfileSchema | None = None

    model_config = {
        "from_attributes": True
    }


class UpdateUserSchema(BaseModel):
    username: str | None = None
    fullname: str | None = None
    key: uuid.UUID | None = None
    work: str | None = None

    model_config = {
        "from_attributes": True,
    }


class LoginSchema(BaseModel):
    username: str
    password: str = Field(default='Stri54_ng')


class RefreshTokenSchema(BaseModel):
    refresh_token: str
