import uuid

from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    username: str
    password: str = Field(default='Stri54_ng')


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class UserCredentialsSchema(BaseModel):
    salt: str
    hashed_password: str
    user_id: int
