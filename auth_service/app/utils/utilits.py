import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.oauth2_scheme import oauth2_scheme
from app.services.jwt_controller import JWT_SECRET_KEY, JWT_ALGORITHM


async def get_user_data_by_username(username: str):
    pass
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(f"http://user_service:8000/api/v1/users/{username}") as resp:
    #         if resp.status != 200:
    #             raise HTTPException(status_code=404, detail="User not found")
    #         return await resp.json()


async def get_payload_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=403, detail="Invalid token type")

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def exception_id(user_id):
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")


async def exception_user_name(user_name):
    if not user_name:
        raise HTTPException(status_code=404, detail="User not found")
