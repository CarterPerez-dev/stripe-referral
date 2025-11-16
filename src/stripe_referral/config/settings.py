"""
ⒸAngelaMos | 2025 | CertGames.com
Application settings with Pydantic
"""

from pydantic_settings import BaseSettings

from .constants import (
    ALLOW_SELF_REFERRAL,
    DEFAULT_PAYOUT_CURRENCY,
    MAX_PAYOUT_AMOUNT,
    MIN_PAYOUT_AMOUNT,
    REQUIRE_RECIPIENT_VALIDATION,
)
from .enums import Environment, LogLevel


class Settings(BaseSettings):
    """
    Application settings loaded from environment
    """
    database_url: str = ""
    stripe_secret_key: str | None = None

    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO

    min_payout_amount: float = MIN_PAYOUT_AMOUNT
    max_payout_amount: float = MAX_PAYOUT_AMOUNT
    default_payout_currency: str = DEFAULT_PAYOUT_CURRENCY

    require_recipient_validation: bool = REQUIRE_RECIPIENT_VALIDATION
    allow_self_referral: bool = ALLOW_SELF_REFERRAL

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "env_prefix": "",
    }


settings = Settings()
