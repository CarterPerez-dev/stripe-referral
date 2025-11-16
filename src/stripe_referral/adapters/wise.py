"""
ⒸAngelaMos | 2025 | CertGames.com
Wise API payout adapter
"""

import uuid
from typing import (
    Any,
    cast,
)

import requests

from ..config.enums import CurrencyCode
from ..exceptions.errors import PayoutAdapterError
from ..schemas.types import (
    PayoutResult,
    RecipientValidation,
)
from .base import PayoutAdapter


class WiseAdapter(PayoutAdapter):
    """
    Payout adapter for Wise API automated transfers
    """
    def __init__(self, api_token: str, sandbox: bool = False) -> None:
        """
        Initialize with Wise API token

        Args:
            api_token: Wise API token
            sandbox: Use sandbox environment if True
        """
        self.api_token = api_token
        self.base_url = (
            "https://api.sandbox.transferwise.tech"
            if sandbox else "https://api.transferwise.com"
        )
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def _make_request(self,
                      method: str,
                      endpoint: str,
                      **kwargs: Any) -> dict[str,
                                             Any]:
        """
        Make HTTP request to Wise API with error handling
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                headers = self.headers,
                timeout = 30,
                **kwargs
            )
            response.raise_for_status()
            json_response: dict[str, Any] = response.json()
            return json_response
        except requests.exceptions.HTTPError as e:
            raise PayoutAdapterError(
                f"Wise API error: {e.response.text}",
                adapter = "wise",
                endpoint = endpoint,
                status_code = e.response.status_code,
            ) from e
        except Exception as e:
            raise PayoutAdapterError(
                f"Wise request error: {str(e)}",
                adapter = "wise",
                endpoint = endpoint,
            ) from e

    def _get_profile_id(self) -> int:
        """
        Get first Wise profile ID
        """
        profiles = self._make_request("GET", "/v1/profiles")
        profiles_list = cast(list[dict[str, Any]], profiles)
        return cast(int, profiles_list[0]["id"])

    def send_payout(
        self,
        user_id: str,
        amount: float,
        currency: str,
        recipient_data: dict[str,
                             Any],
    ) -> PayoutResult:
        """
        Send payout via Wise API
        """
        try:
            profile_id = self._get_profile_id()

            source_currency = recipient_data.get(
                "source_currency",
                CurrencyCode.USD.value
            )
            target_currency = currency

            quote = self._make_request(
                "POST",
                f"/v3/profiles/{profile_id}/quotes",
                json = {
                    "sourceCurrency": source_currency,
                    "targetCurrency": target_currency,
                    "targetAmount": amount,
                    "payOut": "BANK_TRANSFER",
                },
            )

            recipient = self._make_request(
                "POST",
                "/v1/accounts",
                json = {
                    "currency":
                    target_currency,
                    "profile":
                    profile_id,
                    "accountHolderName":
                    recipient_data.get("account_holder_name"),
                    "type":
                    recipient_data.get("account_type",
                                       "aba"),
                    "details":
                    recipient_data.get("details",
                                       {}),
                },
            )

            transfer = self._make_request(
                "POST",
                "/v1/transfers",
                json = {
                    "targetAccount": recipient["id"],
                    "quoteUuid": quote["id"],
                    "customerTransactionId": str(uuid.uuid4()),
                    "details": {
                        "reference":
                        recipient_data.get(
                            "reference",
                            f"Referral payout for {user_id}"
                        ),
                        "transferPurpose":
                        "verification.transfers.purpose.pay.bills",
                        "sourceOfFunds":
                        "verification.source.of.funds.other",
                    },
                },
            )

            self._make_request(
                "POST",
                f"/v3/profiles/{profile_id}/transfers/{transfer['id']}/payments",
                json = {"type": "BALANCE"},
            )

            return PayoutResult(
                success = True,
                transaction_id = str(transfer["id"]),
            )

        except Exception as e:
            return PayoutResult(
                success = False,
                error = str(e),
            )

    def validate_recipient(
        self,
        recipient_data: dict[str,
                             Any]
    ) -> RecipientValidation:
        """
        Validate Wise recipient data
        """
        required_fields = ["account_holder_name", "details"]

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

        account_holder_name = recipient_data.get(
            "account_holder_name",
            ""
        )
        if not account_holder_name or len(account_holder_name) < 2:
            return RecipientValidation(
                valid = False,
                error = "Invalid account holder name",
            )

        details = recipient_data.get("details", {})
        if not isinstance(details, dict):
            return RecipientValidation(
                valid = False,
                error = "Details must be a dictionary",
            )

        account_type = recipient_data.get("account_type", "aba")
        if account_type == "aba":
            if "accountNumber" not in details or "routingNumber" not in details:
                return RecipientValidation(
                    valid = False,
                    error =
                    "Missing accountNumber or routingNumber for ABA transfer",
                )
        elif account_type == "iban" and "iban" not in details:
            return RecipientValidation(
                valid = False,
                error = "Missing IBAN for IBAN transfer",
            )

        return RecipientValidation(valid = True)
