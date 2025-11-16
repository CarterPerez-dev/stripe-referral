"""
ⒸAngelaMos | 2025 | CertGames.com
ReferralCode model
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config.constants import (
    MAX_CODE_LENGTH,
    MAX_USER_ID_LENGTH,
)
from ..config.enums import ReferralCodeStatus
from ..database.Base import (
    Base,
    TimestampMixin,
)

if TYPE_CHECKING:
    from .ReferralProgram import ReferralProgram
    from .ReferralTracking import ReferralTracking


class ReferralCode(Base, TimestampMixin):
    """
    Individual referral code for a user
    """
    __tablename__ = "referral_codes"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        autoincrement = True
    )
    code: Mapped[str] = mapped_column(
        String(MAX_CODE_LENGTH),
        unique = True,
        index = True
    )

    user_id: Mapped[str] = mapped_column(
        String(MAX_USER_ID_LENGTH),
        index = True
    )
    program_id: Mapped[int] = mapped_column(
        ForeignKey("referral_programs.id"),
        nullable = False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default = ReferralCodeStatus.ACTIVE.value,
        index = True
    )

    uses_count: Mapped[int] = mapped_column(Integer, default = 0)
    max_uses: Mapped[int | None] = mapped_column(Integer, nullable = True)

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    program: Mapped[ReferralProgram] = relationship(
        "ReferralProgram",
        back_populates = "codes"
    )
    trackings: Mapped[list[ReferralTracking]] = relationship(
        "ReferralTracking",
        back_populates = "code"
    )
