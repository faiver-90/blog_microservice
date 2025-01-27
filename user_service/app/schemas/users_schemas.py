import uuid

from pydantic import BaseModel, Field, EmailStr


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=5, default='Vladimir')
    full_name: str | None = Field(default='Malashkin')
    email: EmailStr | None = None
    work: str | None = Field(default='Web-developer')

    model_config = {
        "from_attributes": True
    }


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
