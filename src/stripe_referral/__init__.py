"""
ⒸAngelaMos | 2025 | CertGames.com
Framework-agnostic referral program package with Stripe Connect integration
"""

__version__ = "0.1.0"

from .config.settings import settings
from .database.Session import (
    SessionLocal,
    get_db,
)
from .services.payout_service import PayoutService
from .services.referral_service import ReferralService
from .exceptions.errors import (
    CodeExpiredError,
    CodeGenerationError,
    CodeNotFoundError,
    PayoutError,
    ProgramNotFoundError,
    StripeReferralError,
)


__all__ = [
    "ReferralService",
    "PayoutService",
    "SessionLocal",
    "get_db",
    "settings",
    "StripeReferralError",
    "CodeNotFoundError",
    "CodeExpiredError",
    "CodeGenerationError",
    "ProgramNotFoundError",
    "PayoutError",
]
