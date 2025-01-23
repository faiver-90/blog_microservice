from typing import List

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import User
from app.schemas.oauth2_scheme import oauth2_scheme


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    stmt = select(User).options(selectinload(User.userprofile)).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


# async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
#     stmt = select(User).options(selectinload(User.userprofile)).where(User.id == user_id)
#     result = await session.execute(stmt)
#     return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> List[User]:
    stmt = select(User).options(selectinload(User.userprofile))
    result = await session.execute(stmt)
    return result.scalars().all()


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
