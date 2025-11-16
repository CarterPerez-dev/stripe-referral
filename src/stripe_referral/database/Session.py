"""
ⒸAngelaMos | 2025 | CertGames.com
SQLAlchemy session factory and context manager
"""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..config.constants import (
    DATABASE_CONNECTION_MAX_OVERFLOW,
    DATABASE_CONNECTION_POOL_SIZE,
    DATABASE_CONNECTION_TIMEOUT_SECONDS,
)
from ..config.enums import Environment
from ..config.settings import settings


engine: Engine | None
SessionLocal: sessionmaker[Session] | None

if settings.database_url:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping = True,
        pool_size = DATABASE_CONNECTION_POOL_SIZE,
        max_overflow = DATABASE_CONNECTION_MAX_OVERFLOW,
        pool_timeout = DATABASE_CONNECTION_TIMEOUT_SECONDS,
        echo = settings.environment == Environment.DEVELOPMENT,
    )

    SessionLocal = sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine,
    )
else:
    engine = None
    SessionLocal = None


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Database not configured. Set DATABASE_URL environment variable."
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """
    Get a new database session (for dependency injection)
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Database not configured. Set DATABASE_URL environment variable."
        )

    return SessionLocal()
