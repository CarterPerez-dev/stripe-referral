"""
ⒸAngelaMos | 2025 | CertGames.com
Stripe Connect payout adapter
"""

import stripe
from typing import Any

from ..config.constants import (
    STRIPE_API_VERSION,
    STRIPE_CONNECT_ACCOUNT_ID_PREFIX,
    STRIPE_TRANSFER_ID_PREFIX,
)
from ..schemas.types import (
    PayoutResult,
    RecipientValidation,
)
from .base import PayoutAdapter


class StripeConnectAdapter(PayoutAdapter):
    """
    Payout adapter for Stripe Connect transfers
    """
    def __init__(self, api_key: str) -> None:
        """
        Initialize with Stripe API key

        Args:
            api_key: Stripe secret key
        """
        self.api_key = api_key
        stripe.api_key = api_key
        stripe.api_version = STRIPE_API_VERSION

    def send_payout(
        self,
        user_id: str,
        amount: float,
        currency: str,
        recipient_data: dict[str,
                             Any],
    ) -> PayoutResult:
        """
        Send payout via Stripe Connect transfer
        """
        try:
            connected_account_id = recipient_data.get(
                "stripe_connect_account_id"
            )
            if not connected_account_id:
                return PayoutResult(
                    success = False,
                    error =
                    "Missing stripe_connect_account_id in recipient_data",
                )

            if not connected_account_id.startswith(
                    STRIPE_CONNECT_ACCOUNT_ID_PREFIX):
                return PayoutResult(
                    success = False,
                    error =
                    f"Invalid Stripe account ID format: {connected_account_id}",
                )

            amount_cents = int(amount * 100)

            transfer = stripe.Transfer.create(
                amount = amount_cents,
                currency = currency.lower(),
                destination = connected_account_id,
                metadata = {"user_id": user_id},
            )

            if not transfer.id.startswith(STRIPE_TRANSFER_ID_PREFIX):
                return PayoutResult(
                    success = False,
                    error =
                    f"Unexpected transfer ID format: {transfer.id}",
                )

            return PayoutResult(
                success = True,
                transaction_id = transfer.id,
            )

        except stripe.InvalidRequestError as e:
            return PayoutResult(
                success = False,
                error = f"Invalid request: {str(e)}",
            )
        except stripe.AuthenticationError as e:
            return PayoutResult(
                success = False,
                error = f"Authentication failed: {str(e)}",
            )
        except stripe.StripeError as e:
            return PayoutResult(
                success = False,
                error = f"Stripe error: {str(e)}",
            )
        except Exception as e:
            return PayoutResult(
                success = False,
                error = f"Unexpected error: {str(e)}",
            )

    def validate_recipient(
        self,
        recipient_data: dict[str,
                             Any]
    ) -> RecipientValidation:
        """
        Validate Stripe Connect account exists and can receive payouts
        """
        try:
            account_id = recipient_data.get("stripe_connect_account_id")
            if not account_id:
                return RecipientValidation(
                    valid = False,
                    error = "Missing stripe_connect_account_id",
                )

            if not account_id.startswith(STRIPE_CONNECT_ACCOUNT_ID_PREFIX
                                         ):
                return RecipientValidation(
                    valid = False,
                    error = f"Invalid account ID format: {account_id}",
                )

            account = stripe.Account.retrieve(account_id)

            if not account.payouts_enabled:
                return RecipientValidation(
                    valid = False,
                    error = "Payouts not enabled for this Stripe account",
                )

            if not account.charges_enabled:
                return RecipientValidation(
                    valid = False,
                    error = "Account not fully activated",
                )

            return RecipientValidation(valid = True)

        except stripe.InvalidRequestError as e:
            return RecipientValidation(
                valid = False,
                error = f"Invalid account: {str(e)}",
            )
        except stripe.StripeError as e:
            return RecipientValidation(
                valid = False,
                error = f"Stripe error: {str(e)}",
            )
        except Exception as e:
            return RecipientValidation(
                valid = False,
                error = f"Validation error: {str(e)}",
            )
