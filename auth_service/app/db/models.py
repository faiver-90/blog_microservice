from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserCredentials(Base):
    __tablename__ = "auth_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    salt: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Auth(id={self.id!r}, user_id={self.user_id!r})"
