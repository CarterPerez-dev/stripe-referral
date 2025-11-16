"""
ⒸAngelaMos | 2025 | CertGames.com
Manual payout adapter for bank transfers
"""

from typing import Any

from ..config.constants import (
    MANUAL_PAYOUT_ID_PREFIX,
)
from ..schemas.types import (
    PayoutResult,
    RecipientValidation,
)
from .base import PayoutAdapter


class ManualBankAdapter(PayoutAdapter):
    """
    Manual bank transfer adapter for admin processed payouts
    """
    def send_payout(
        self,
        user_id: str,
        amount: float,
        _currency: str,
        _recipient_data: dict[str,
                              Any],
    ) -> PayoutResult:
        """
        Mark payout as pending manual review and processing
        """
        transaction_id = f"{MANUAL_PAYOUT_ID_PREFIX}{user_id}_{int(amount * 100)}"

        return PayoutResult(
            success = True,
            transaction_id = transaction_id,
        )

    def validate_recipient(
        self,
        recipient_data: dict[str,
                             Any]
    ) -> RecipientValidation:
        """
        Validate bank account information is present
        """
        required_fields = [
            "bank_account_number",
            "routing_number",
            "account_holder_name",
        ]

        missing_fields = [
            field for field in required_fields
            if field not in recipient_data
        ]

        if missing_fields:
            return RecipientValidation(
                valid = False,
                error =
                f"Missing required fields: {', '.join(missing_fields)}",
            )

        account_number = recipient_data.get("bank_account_number", "")
        if not account_number or len(account_number) < 4:
            return RecipientValidation(
                valid = False,
                error = "Invalid bank account number",
            )

        routing_number = recipient_data.get("routing_number", "")
        if not routing_number or len(routing_number) != 9:
            return RecipientValidation(
                valid = False,
                error = "Invalid routing number (must be 9 digits)",
            )

        account_holder_name = recipient_data.get(
            "account_holder_name",
            ""
        )
        if not account_holder_name or len(account_holder_name) < 2:
            return RecipientValidation(
                valid = False,
                error = "Invalid account holder name",
            )

        return RecipientValidation(valid = True)
