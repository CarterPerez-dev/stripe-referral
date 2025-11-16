"""
ⒸAngelaMos | 2025 | CertGames.com
Payout repository
"""

from datetime import (
    UTC,
    datetime,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config.enums import PayoutStatus
from ..models.Payout import Payout

from .base import BaseRepository


class PayoutRepository(BaseRepository[Payout]):
    """
    Repository for Payout database operations
    """
    def __init__(self, db: Session) -> None:
        """
        Initialize with Payout model
        """
        super().__init__(db, Payout)

    def get_by_user(self, user_id: str) -> list[Payout]:
        """
        Get all payouts for a user
        """
        stmt = select(Payout).where(Payout.user_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_tracking_id(self, tracking_id: int) -> Payout | None:
        """
        Get payout by tracking ID
        """
        stmt = select(Payout).where(Payout.tracking_id == tracking_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_pending_payouts(self,
                            limit: int | None = None) -> list[Payout]:
        """
        Get all pending payouts with optional limit
        """
        stmt = select(Payout).where(
            Payout.status == PayoutStatus.PENDING.value
        )
        if limit:
            stmt = stmt.limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def get_failed_payouts(self,
                           limit: int | None = None) -> list[Payout]:
        """
        Get all failed payouts with optional limit
        """
        stmt = select(Payout).where(
            Payout.status == PayoutStatus.FAILED.value
        )
        if limit:
            stmt = stmt.limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def mark_as_paid(
        self,
        payout_id: int,
        transaction_id: str
    ) -> Payout | None:
        """
        Mark payout as paid with transaction ID
        """
        payout = self.get_by_id(payout_id)
        if not payout:
            return None

        payout.status = PayoutStatus.PAID.value
        payout.external_transaction_id = transaction_id
        payout.processed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(payout)
        return payout

    def mark_as_failed(
        self,
        payout_id: int,
        error_message: str
    ) -> Payout | None:
        """
        Mark payout as failed with error message
        """
        payout = self.get_by_id(payout_id)
        if not payout:
            return None

        payout.status = PayoutStatus.FAILED.value
        payout.error_message = error_message
        payout.failed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(payout)
        return payout
