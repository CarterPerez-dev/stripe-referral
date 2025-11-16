"""
ⒸAngelaMos | 2025 | CertGames.com
All magic strings as enums
"""

from enum import Enum


class PayoutStatus(str, Enum):
    """
    Payout status values
    """
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReferralCodeStatus(str, Enum):
    """
    Referral code status values
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class ReferralTrackingStatus(str, Enum):
    """
    Referral tracking payout status
    """
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class AdapterType(str, Enum):
    """
    Payout adapter types
    """
    STRIPE_CONNECT = "stripe_connect"
    MANUAL = "manual"
    WISE = "wise"
    PAYPAL = "paypal"


class RewardType(str, Enum):
    """
    Referral reward types
    """
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    PERCENTAGE = "percentage"
    TIERED = "tiered"


class CurrencyCode(str, Enum):
    """
    Supported currency codes (ISO 4217)
    """
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"


class Environment(str, Enum):
    """
    Application environment
    """
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """
    Logging level
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
