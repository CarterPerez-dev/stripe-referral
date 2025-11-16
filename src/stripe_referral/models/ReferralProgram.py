"""
ⒸAngelaMos | 2025 | CertGames.com
ReferralProgram model
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
)

from sqlalchemy import (
    JSON,
    Boolean,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config.constants import (
    MAX_PROGRAM_KEY_LENGTH,
    MAX_PROGRAM_NAME_LENGTH,
)
from ..config.enums import (
    AdapterType,
    CurrencyCode,
    RewardType,
)
from ..database.Base import (
    Base,
    TimestampMixin,
)

if TYPE_CHECKING:
    from .ReferralCode import ReferralCode
    from .ReferralTracking import ReferralTracking


class ReferralProgram(Base, TimestampMixin):
    """
    Referral program configuration
    """
    __tablename__ = "referral_programs"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )
    name: Mapped[str] = mapped_column(
        String(MAX_PROGRAM_NAME_LENGTH),
        unique = True,
        index = True
    )
    program_key: Mapped[str] = mapped_column(
        String(MAX_PROGRAM_KEY_LENGTH),
        unique = True,
        index = True
    )

    reward_amount: Mapped[float] = mapped_column(Float, nullable = False)
    reward_currency: Mapped[str] = mapped_column(
        String(3),
        default = CurrencyCode.USD.value
    )
    reward_type: Mapped[str] = mapped_column(
        String(50),
        default = RewardType.ONE_TIME.value
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    max_rewards_per_user: Mapped[int | None] = mapped_column(
        Integer,
        nullable = True
    )
    conversion_window_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable = True
    )

    adapter_type: Mapped[str] = mapped_column(
        String(50),
        default = AdapterType.MANUAL.value
    )
    adapter_config: Mapped[dict[str,
                                Any]] = mapped_column(
                                    JSON,
                                    default = dict
                                )

    codes: Mapped[list[ReferralCode]] = relationship(
        "ReferralCode",
        back_populates = "program",
        cascade = "all, delete-orphan"
    )
    trackings: Mapped[list[ReferralTracking]] = relationship(
        "ReferralTracking",
        back_populates = "program"
    )
