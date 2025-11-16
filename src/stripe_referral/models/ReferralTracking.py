"""
ⒸAngelaMos | 2025 | CertGames.com
ReferralTracking model
"""

from __future__ import annotations

from datetime import (
    UTC,
    datetime,
)
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config.constants import (
    MAX_TRANSACTION_ID_LENGTH,
    MAX_USER_ID_LENGTH,
)
from ..config.enums import (
    CurrencyCode,
    ReferralTrackingStatus,
)
from ..database.Base import (
    Base,
    TimestampMixin,
)

if TYPE_CHECKING:
    from .Payout import Payout
    from .ReferralCode import ReferralCode
    from .ReferralProgram import ReferralProgram


class ReferralTracking(Base, TimestampMixin):
    """
    Tracks successful referral conversions
    """
    __tablename__ = "referral_trackings"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    referrer_user_id: Mapped[str] = mapped_column(
        String(MAX_USER_ID_LENGTH),
        index = True
    )
    referred_user_id: Mapped[str] = mapped_column(
        String(MAX_USER_ID_LENGTH),
        index = True
    )

    code_id: Mapped[int] = mapped_column(
        ForeignKey("referral_codes.id"),
        nullable = False
    )
    program_id: Mapped[int] = mapped_column(
        ForeignKey("referral_programs.id"),
        nullable = False
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(MAX_TRANSACTION_ID_LENGTH),
        nullable = True
    )
    transaction_amount: Mapped[float | None] = mapped_column(
        Float,
        nullable = True
    )

    amount_earned: Mapped[float] = mapped_column(Float, nullable = False)
    currency: Mapped[str] = mapped_column(
        String(3),
        default = CurrencyCode.USD.value
    )

    converted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda: datetime.now(UTC),
        index = True
    )

    payout_status: Mapped[str] = mapped_column(
        String(20),
        default = ReferralTrackingStatus.PENDING.value,
        index = True
    )

    code: Mapped[ReferralCode] = relationship(
        "ReferralCode",
        back_populates = "trackings"
    )
    program: Mapped[ReferralProgram] = relationship(
        "ReferralProgram",
        back_populates = "trackings"
    )
    payout: Mapped[Payout | None] = relationship(
        "Payout",
        back_populates = "tracking",
        uselist = False
    )
