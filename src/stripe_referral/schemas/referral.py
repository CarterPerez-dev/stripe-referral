"""
ⒸAngelaMos | 2025 | CertGames.com
Pydantic schemas for referral operations
"""

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from ..config.constants import (
    MAX_CODE_LENGTH,
    MAX_PROGRAM_KEY_LENGTH,
    MAX_TRANSACTION_ID_LENGTH,
    MAX_USER_ID_LENGTH,
    MIN_PAYOUT_AMOUNT,
)


class CreateCodeRequest(BaseModel):
    """
    Request schema for creating referral code
    """
    user_id: str = Field(
        ...,
        min_length = 1,
        max_length = MAX_USER_ID_LENGTH
    )
    program_key: str = Field(
        ...,
        min_length = 1,
        max_length = MAX_PROGRAM_KEY_LENGTH
    )

    @field_validator("user_id", "program_key")
    @classmethod
    def validate_no_whitespace(cls, v: str) -> str:
        """
        Ensure no leading/trailing whitespace
        """
        return v.strip()


class CreateCodeResponse(BaseModel):
    """
    Response schema for code creation
    """
    code: str
    program_id: int
    user_id: str
    created_at: str


class TrackReferralRequest(BaseModel):
    """
    Request schema for tracking referral conversion
    """
    code: str = Field(..., min_length = 1, max_length = MAX_CODE_LENGTH)
    referred_user_id: str = Field(
        ...,
        min_length = 1,
        max_length = MAX_USER_ID_LENGTH
    )
    transaction_id: str | None = Field(
        None,
        max_length = MAX_TRANSACTION_ID_LENGTH
    )
    transaction_amount: float | None = Field(None, ge = MIN_PAYOUT_AMOUNT)

    @field_validator("code", "referred_user_id")
    @classmethod
    def validate_no_whitespace(cls, v: str) -> str:
        """
        Ensure no leading/trailing whitespace
        """
        return v.strip()


class TrackReferralResponse(BaseModel):
    """
    Response schema for referral tracking
    """
    tracking_id: int
    referrer_user_id: str
    referred_user_id: str
    amount_earned: float
    currency: str
    converted_at: str


class UserEarningsResponse(BaseModel):
    """
    Response schema for user earnings
    """
    total: float
    pending: float
    paid: float


class CodeValidationResponse(BaseModel):
    """
    Response schema for code validation
    """
    valid: bool
    code_id: int | None = None
    program_id: int | None = None
    referrer_user_id: str | None = None
    reason: str | None = None


class ReferralHistoryResponse(BaseModel):
    """
    Response schema for referral history
    """
    referred_user_id: str
    amount_earned: float
    currency: str
    converted_at: str
    payout_status: str
