import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException

from app.schemas.auth_schemas import RefreshTokenSchema

load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


class JWTController:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def create_access_token(self, data: dict, expires_in) -> str:
        """Создает JWT-токен с данными."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(seconds=expires_in)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def refresh_access_token(self, token: RefreshTokenSchema) -> dict:
        payload = await self.decode_access_token(token)
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=403, detail='Invalid token type')

        updated_payload = {
            **payload,
            "type": "access"
        }
        new_access_token = await self.create_access_token(updated_payload, expires_in=3600)
        return {"access_token": new_access_token}


async def get_jwt_controller() -> JWTController:
    return JWTController(JWT_SECRET_KEY, JWT_ALGORITHM)
