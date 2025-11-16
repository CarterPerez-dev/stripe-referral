"""
ⒸAngelaMos | 2025 | CertGames.com
Custom exception hierarchy for stripe referral
"""

from typing import Any


class StripeReferralError(Exception):
    """
    Base exception for all stripe referral errors
    """
    def __init__(self, message: str, **context: Any) -> None:
        super().__init__(message)
        self.message = message
        self.context = context

    def __str__(self) -> str:
        if self.context:
            context_str = ", ".join(
                f"{k}={v}" for k, v in self.context.items()
            )
            return f"{self.message} ({context_str})"
        return self.message


class ValidationError(StripeReferralError):
    """
    Raised when input validation fails
    """


class CodeNotFoundError(StripeReferralError):
    """
    Raised when referral code does not exist
    """


class CodeExpiredError(StripeReferralError):
    """
    Raised when referral code has expired
    """


class CodeInactiveError(StripeReferralError):
    """
    Raised when referral code is inactive or suspended
    """


class CodeMaxUsesReachedError(StripeReferralError):
    """
    Raised when referral code has reached maximum uses
    """


class ProgramNotFoundError(StripeReferralError):
    """
    Raised when referral program does not exist
    """


class ProgramInactiveError(StripeReferralError):
    """
    Raised when referral program is inactive
    """


class PayoutError(StripeReferralError):
    """
    Base exception for payout-related errors
    """


class PayoutAdapterError(PayoutError):
    """
    Raised when payout adapter fails
    """


class RecipientValidationError(PayoutError):
    """
    Raised when recipient data validation fails
    """


class InsufficientFundsError(PayoutError):
    """
    Raised when payout amount exceeds available balance
    """


class DuplicateReferralError(StripeReferralError):
    """
    Raised when attempting to track duplicate referral
    """


class SelfReferralError(StripeReferralError):
    """
    Raised when user attempts to refer themselves
    """


class DatabaseError(StripeReferralError):
    """
    Raised when database operation fails
    """


class ConfigurationError(StripeReferralError):
    """
    Raised when configuration is invalid or missing
    """


class StripeAPIError(PayoutError):
    """
    Raised when Stripe API call fails
    """


class CodeGenerationError(StripeReferralError):
    """
    Raised when unable to generate unique referral code after max attempts
    """


class PayoutNotFoundError(PayoutError):
    """
    Raised when payout record does not exist
    """


class PayoutAlreadyExistsError(PayoutError):
    """
    Raised when payout already exists for a tracking entry
    """


class TrackingNotFoundError(StripeReferralError):
    """
    Raised when tracking record does not exist
    """


class InvalidRecipientDataError(PayoutError):
    """
    Raised when recipient data is invalid or incomplete
    """
