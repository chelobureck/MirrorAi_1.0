from __future__ import annotations
from typing import Optional
from datetime import datetime
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer



from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from models.database import Base

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], default="argon2", deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme_optional = HTTPBearer(auto_error=False)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="user")  # user, admin
    credits: Mapped[int] = mapped_column(Integer, default=100)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email_verification_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    email_verification_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    presentations = relationship("Presentation", back_populates="user")
    boards = relationship("Board", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)

    # Методы для работы с паролем
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет пароль, используя CryptContext (теперь Argon2)."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Создает хеш пароля, используя CryptContext (теперь Argon2)."""
        return pwd_context.hash(password)
