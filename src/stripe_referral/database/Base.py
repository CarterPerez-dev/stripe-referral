"""
ⒸAngelaMos | 2025 | CertGames.com
SQLAlchemy declarative base and timestamp mixin
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    """
    Base model for all tables
    """


class TimestampMixin:
    """
    Mixin for created_at and updated_at timestamps
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(UTC),
        nullable = False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(UTC),
        onupdate = lambda: datetime.now(UTC),
        nullable = False,
    )
