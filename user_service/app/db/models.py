from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid


class Base(AsyncAttrs, DeclarativeBase):
    pass


# ========================================User==========================================================================
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    # id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    key: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True, default=uuid.uuid4)
    userprofile: Mapped[Optional["UserProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan",
                                                                uselist=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.fullname!r})"


class UserProfile(Base):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="userprofile")
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE"))
    work: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Добавлено поле

    def __repr__(self) -> str:
        return f"UserProfile(id={self.id!r}, user_id={self.user_id!r})"
