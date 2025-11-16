"""
ⒸAngelaMos | 2025 | CertGames.com
Pydantic schemas for payout operations
"""

from typing import Any

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)
from ..config.constants import (
    CURRENCY_CODE_LENGTH,
    MAX_CONVERSION_WINDOW_DAYS,
    MAX_MAX_REWARDS_PER_USER,
    MAX_PROGRAM_KEY_LENGTH,
    MAX_PROGRAM_NAME_LENGTH,
    MAX_USER_ID_LENGTH,
    MIN_CONVERSION_WINDOW_DAYS,
    MIN_MAX_REWARDS_PER_USER,
    MIN_PAYOUT_AMOUNT,
    MIN_REWARD_AMOUNT,
)
from ..config.enums import (
    AdapterType,
    CurrencyCode,
    RewardType,
)


class ProcessPayoutRequest(BaseModel):
    """
    Request schema for processing payout
    """
    user_id: str = Field(
        ...,
        min_length = 1,
        max_length = MAX_USER_ID_LENGTH
    )
    amount: float = Field(..., ge = MIN_PAYOUT_AMOUNT)
    recipient_data: dict[str, Any]

    @field_validator("user_id")
    @classmethod
    def validate_no_whitespace(cls, v: str) -> str:
        """
        Ensure no leading/trailing whitespace
        """
        return v.strip()


class ProcessPayoutResponse(BaseModel):
    """
    Response schema for payout processing
    """
    success: bool
    transaction_id: str | None = None
    error: str | None = None


class RecipientValidationRequest(BaseModel):
    """
    Request schema for recipient validation
    """
    recipient_data: dict[str, Any]


class RecipientValidationResponse(BaseModel):
    """
    Response schema for recipient validation
    """
    valid: bool
    error: str | None = None


class PayoutInfoResponse(BaseModel):
    """
    Response schema for payout information
    """
    id: int
    user_id: str
    amount: float
    currency: str
    status: str
    adapter_type: str
    processed_at: str | None = None
    external_transaction_id: str | None = None


class CreateProgramRequest(BaseModel):
    """
    Request schema for creating referral program
    """
    name: str = Field(
        ...,
        min_length = 1,
        max_length = MAX_PROGRAM_NAME_LENGTH
    )
    program_key: str = Field(
        ...,
        min_length = 1,
        max_length = MAX_PROGRAM_KEY_LENGTH
    )
    reward_amount: float = Field(..., ge = MIN_REWARD_AMOUNT)
    reward_currency: str = Field(
        default = CurrencyCode.USD.value,
        min_length = CURRENCY_CODE_LENGTH,
        max_length = CURRENCY_CODE_LENGTH
    )
    reward_type: str = Field(default = RewardType.ONE_TIME.value)
    adapter_type: str = Field(default = AdapterType.MANUAL.value)
    max_rewards_per_user: int | None = Field(
        None,
        ge = MIN_MAX_REWARDS_PER_USER,
        le = MAX_MAX_REWARDS_PER_USER
    )
    conversion_window_days: int | None = Field(
        None,
        ge = MIN_CONVERSION_WINDOW_DAYS,
        le = MAX_CONVERSION_WINDOW_DAYS
    )

    @field_validator("name", "program_key")
    @classmethod
    def validate_no_whitespace(cls, v: str) -> str:
        """
        Ensure no leading/trailing whitespace
        """
        return v.strip()

    @field_validator("reward_currency")
    @classmethod
    def validate_currency_uppercase(cls, v: str) -> str:
        """
        Ensure currency is uppercase
        """
        return v.upper()


class ProgramInfoResponse(BaseModel):
    """
    Response schema for program information
    """
    id: int
    name: str
    program_key: str
    reward_amount: float
    reward_currency: str
    reward_type: str
    is_active: bool
