"""
ⒸAngelaMos | 2025 | CertGames.com
Schema exports
"""

from .referral import (
    CreateCodeRequest,
    CreateCodeResponse,
    TrackReferralRequest,
    TrackReferralResponse,
    UserEarningsResponse,
    CodeValidationResponse,
    ReferralHistoryResponse,
)
from .payout import (
    ProcessPayoutRequest,
    ProcessPayoutResponse,
    RecipientValidationRequest,
    RecipientValidationResponse,
    PayoutInfoResponse,
    CreateProgramRequest,
    ProgramInfoResponse,
)
from .types import (
    CreateCodeResult,
    TrackReferralResult,
    UserEarnings,
    CodeValidation,
    PayoutResult,
    RecipientValidation,
    ReferralHistoryItem,
    ProgramInfo,
    PayoutInfo,
)


__all__ = [
    "CreateCodeRequest",
    "CreateCodeResponse",
    "TrackReferralRequest",
    "TrackReferralResponse",
    "UserEarningsResponse",
    "CodeValidationResponse",
    "ReferralHistoryResponse",
    "ProcessPayoutRequest",
    "ProcessPayoutResponse",
    "RecipientValidationRequest",
    "RecipientValidationResponse",
    "PayoutInfoResponse",
    "CreateProgramRequest",
    "ProgramInfoResponse",
    "CreateCodeResult",
    "TrackReferralResult",
    "UserEarnings",
    "CodeValidation",
    "PayoutResult",
    "RecipientValidation",
    "ReferralHistoryItem",
    "ProgramInfo",
    "PayoutInfo",
]
