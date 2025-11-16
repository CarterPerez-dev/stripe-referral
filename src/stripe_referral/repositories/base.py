"""
ⒸAngelaMos | 2025 | CertGames.com
Base repository with generic CRUD operations
"""

from typing import (
    Any,
    Generic,
    TypeVar,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database.Base import Base


T = TypeVar("T", bound = Base)


class BaseRepository(Generic[T]):
    """
    Base repository with common CRUD operations
    """
    def __init__(self, db: Session, model: type[T]) -> None:
        """
        Initialize repository with database session and model type
        """
        self.db = db
        self.model = model

    def create(self, **kwargs: Any) -> T:
        """
        Create a new record
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_by_id(self, record_id: int) -> T | None:
        """
        Get record by ID
        """
        return self.db.get(self.model, record_id)

    def get_all(self,
                limit: int | None = None,
                offset: int = 0) -> list[T]:
        """
        Get all records with pagination
        """
        stmt = select(self.model).offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def update(self, record_id: int, **kwargs: Any) -> T | None:
        """
        Update record by ID
        """
        instance = self.get_by_id(record_id)
        if not instance:
            return None

        for key, value in kwargs.items():
            setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, record_id: int) -> bool:
        """
        Delete record by ID
        """
        instance = self.get_by_id(record_id)
        if not instance:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True
