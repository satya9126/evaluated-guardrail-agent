from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    request_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    prompt_injection_detected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    pii_detected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    model_used: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    response_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )