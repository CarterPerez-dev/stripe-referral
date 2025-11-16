"""
ⒸAngelaMos | 2025 | CertGames.com
Payout model
"""

from __future__ import annotations

from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
)

from sqlalchemy import (
    JSON,
    Float,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config.constants import (
    MAX_ERROR_MESSAGE_LENGTH,
    MAX_TRANSACTION_ID_LENGTH,
    MAX_USER_ID_LENGTH,
)
from ..config.enums import (
    CurrencyCode,
    PayoutStatus,
)
from ..database.Base import (
    Base,
    TimestampMixin,
)

if TYPE_CHECKING:
    from .ReferralTracking import ReferralTracking


class Payout(Base, TimestampMixin):
    """
    Payout record for referral rewards
    """
    __tablename__ = "payouts"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )

    user_id: Mapped[str] = mapped_column(
        String(MAX_USER_ID_LENGTH),
        index = True
    )
    tracking_id: Mapped[int] = mapped_column(
        ForeignKey("referral_trackings.id"),
        nullable = False,
        unique = True
    )

    amount: Mapped[float] = mapped_column(Float, nullable = False)
    currency: Mapped[str] = mapped_column(
        String(3),
        default = CurrencyCode.USD.value
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default = PayoutStatus.PENDING.value,
        index = True
    )

    adapter_type: Mapped[str] = mapped_column(
        String(50),
        nullable = False
    )
    recipient_data: Mapped[dict[str,
                                Any]] = mapped_column(
                                    JSON,
                                    default = dict
                                )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )
    failed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    external_transaction_id: Mapped[str | None] = mapped_column(
        String(MAX_TRANSACTION_ID_LENGTH),
        nullable = True
    )
    error_message: Mapped[str | None] = mapped_column(
        String(MAX_ERROR_MESSAGE_LENGTH),
        nullable = True
    )

    tracking: Mapped[ReferralTracking] = relationship(
        "ReferralTracking",
        back_populates = "payout"
    )
