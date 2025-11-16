"""
ⒸAngelaMos | 2025 | CertGames.com
Referral code and tracking repositories
"""

from sqlalchemy import (
    case,
    func,
    select,
)
from sqlalchemy.orm import Session

from ..config.enums import ReferralTrackingStatus
from ..models.ReferralCode import ReferralCode
from ..models.ReferralTracking import ReferralTracking

from .base import BaseRepository


class ReferralCodeRepository(BaseRepository[ReferralCode]):
    """
    Repository for ReferralCode database operations
    """
    def __init__(self, db: Session) -> None:
        """
        Initialize with ReferralCode model
        """
        super().__init__(db, ReferralCode)

    def get_by_code(self, code: str) -> ReferralCode | None:
        """
        Get referral code by code string
        """
        stmt = select(ReferralCode).where(ReferralCode.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_user(self,
                    user_id: str,
                    program_id: int | None = None) -> list[ReferralCode]:
        """
        Get all codes for a user optionally filtered by program
        """
        stmt = select(ReferralCode).where(ReferralCode.user_id == user_id)
        if program_id:
            stmt = stmt.where(ReferralCode.program_id == program_id)
        return list(self.db.execute(stmt).scalars().all())

    def increment_uses(self, code_id: int) -> bool:
        """
        Atomically increment uses count
        """
        code = self.get_by_id(code_id)
        if not code:
            return False

        code.uses_count += 1
        self.db.commit()
        return True


class ReferralTrackingRepository(BaseRepository[ReferralTracking]):
    """
    Repository for ReferralTracking database operations
    """
    def __init__(self, db: Session) -> None:
        """
        Initialize with ReferralTracking model
        """
        super().__init__(db, ReferralTracking)

    def get_by_referrer(self, user_id: str) -> list[ReferralTracking]:
        """
        Get all referral conversions for a referrer
        """
        stmt = select(ReferralTracking).where(
            ReferralTracking.referrer_user_id == user_id
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_pending_payouts(self,
                            program_id: int | None = None
                            ) -> list[ReferralTracking]:
        """
        Get all tracking records with pending payouts
        """
        stmt = select(ReferralTracking).where(
            ReferralTracking.payout_status ==
            ReferralTrackingStatus.PENDING.value
        )
        if program_id:
            stmt = stmt.where(ReferralTracking.program_id == program_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_user_earnings(self, user_id: str) -> dict[str, float]:
        """
        Calculate total earnings for a user
        """
        stmt = select(
            func.sum(ReferralTracking.amount_earned).label("total"),
            func.sum(
                case(
                    (
                        ReferralTracking.payout_status
                        == ReferralTrackingStatus.PENDING.value,
                        ReferralTracking.amount_earned,
                    ),
                    else_ = 0,
                )
            ).label("pending"),
            func.sum(
                case(
                    (
                        ReferralTracking.payout_status
                        == ReferralTrackingStatus.PAID.value,
                        ReferralTracking.amount_earned,
                    ),
                    else_ = 0,
                )
            ).label("paid"),
        ).where(ReferralTracking.referrer_user_id == user_id)

        result = self.db.execute(stmt).one()
        return {
            "total": float(result.total or 0),
            "pending": float(result.pending or 0),
            "paid": float(result.paid or 0),
        }
