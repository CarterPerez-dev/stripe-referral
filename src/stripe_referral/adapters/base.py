"""
ⒸAngelaMos | 2025 | CertGames.com
Base payout adapter interface
"""

from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from ..schemas.types import (
    PayoutResult,
    RecipientValidation,
)


class PayoutAdapter(ABC):
    """
    Abstract base class for payout adapters
    """
    @abstractmethod
    def send_payout(
        self,
        user_id: str,
        amount: float,
        currency: str,
        recipient_data: dict[str,
                             Any],
    ) -> PayoutResult:
        """
        Process a payout to the user

        Args:
            user_id: User identifier
            amount: Amount to send
            currency: Currency code
            recipient_data: Recipient information

        Returns:
            PayoutResult TypedDict with 
            success bool and transaction_id or error
        """

    @abstractmethod
    def validate_recipient(
        self,
        recipient_data: dict[str,
                             Any]
    ) -> RecipientValidation:
        """
        Validate recipient data before attempting payout

        Args:
            recipient_data: Recipient information to validate

        Returns:
            RecipientValidation TypedDict with 
            valid bool and error if invalid
        """
