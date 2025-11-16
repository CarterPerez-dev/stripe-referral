"""
ⒸAngelaMos | 2025 | CertGames.com
TypedDict definitions for service return types
"""

from typing import (
    TypedDict,
    NotRequired,
)


class CreateCodeResult(TypedDict):
    """
    Return type for ReferralService.create_code()
    """
    code: str
    program_id: int
    user_id: str
    created_at: str


class TrackReferralResult(TypedDict):
    """
    Return type for ReferralService.track_referral()
    """
    tracking_id: int
    referrer_user_id: str
    referred_user_id: str
    amount_earned: float
    currency: str
    converted_at: str


class UserEarnings(TypedDict):
    """
    Return type for earnings queries
    """
    total: float
    pending: float
    paid: float


class CodeValidation(TypedDict):
    """
    Return type for code validation
    """
    valid: bool
    code_id: NotRequired[int]
    program_id: NotRequired[int]
    referrer_user_id: NotRequired[str]
    reason: NotRequired[str]


class PayoutResult(TypedDict):
    """
    Return type for payout operations
    """
    success: bool
    transaction_id: NotRequired[str]
    error: NotRequired[str]


class RecipientValidation(TypedDict):
    """
    Return type for recipient validation
    """
    valid: bool
    error: NotRequired[str]


class ReferralHistoryItem(TypedDict):
    """
    Single referral history record
    """
    referred_user_id: str
    amount_earned: float
    currency: str
    converted_at: str
    payout_status: str


class ProgramInfo(TypedDict):
    """
    Return type for program information
    """
    id: int
    name: str
    program_key: str
    reward_amount: float
    reward_currency: str
    reward_type: str
    is_active: bool


class PayoutInfo(TypedDict):
    """
    Return type for payout information
    """
    id: int
    user_id: str
    amount: float
    currency: str
    status: str
    adapter_type: str
    processed_at: str | None
    external_transaction_id: str | None
