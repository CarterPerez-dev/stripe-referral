"""
ⒸAngelaMos | 2025 | CertGames.com
Payout service with business logic
"""

from typing import Any
from sqlalchemy.orm import Session

from ..adapters import (
    ManualBankAdapter,
    PayoutAdapter,
    StripeConnectAdapter,
    WiseAdapter,
)
from ..config.enums import (
    AdapterType,
    CurrencyCode,
    PayoutStatus,
    RewardType,
)
from ..exceptions.errors import (
    InvalidRecipientDataError,
    PayoutAlreadyExistsError,
    PayoutNotFoundError,
    TrackingNotFoundError,
)
from ..repositories.payout_repo import PayoutRepository
from ..repositories.program_repo import ReferralProgramRepository
from ..repositories.referral_repo import ReferralTrackingRepository
from ..schemas.types import (
    PayoutInfo,
    PayoutResult,
    ProgramInfo,
    RecipientValidation,
)


class PayoutService:
    """
    Service for payout business logic
    """
    @staticmethod
    def _get_adapter(
        adapter_type: str,
        adapter_config: dict[str,
                             Any] | None = None
    ) -> PayoutAdapter:
        """
        Factory method to get the appropriate payout adapter instance
        """
        config = adapter_config or {}

        if adapter_type == AdapterType.MANUAL.value:
            return ManualBankAdapter()
        if adapter_type == AdapterType.STRIPE_CONNECT.value:
            api_key = config.get("api_key", "")
            return StripeConnectAdapter(api_key = api_key)
        if adapter_type == AdapterType.WISE.value:
            api_token = config.get("api_token", "")
            sandbox = config.get("sandbox", False)
            return WiseAdapter(api_token = api_token, sandbox = sandbox)

        raise InvalidRecipientDataError(
            f"Unknown adapter type: {adapter_type}",
            adapter_type = adapter_type,
        )

    @staticmethod
    def create_program(
        db: Session,
        name: str,
        program_key: str,
        reward_amount: float,
        *,
        reward_currency: str = CurrencyCode.USD.value,
        reward_type: str = RewardType.ONE_TIME.value,
        adapter_type: str = AdapterType.MANUAL.value,
        max_rewards_per_user: int | None = None,
        conversion_window_days: int | None = None,
        adapter_config: dict[str,
                             Any] | None = None,
    ) -> ProgramInfo:
        """
        Create a new referral program
        """
        valid_adapter_types = [at.value for at in AdapterType]
        if adapter_type not in valid_adapter_types:
            raise InvalidRecipientDataError(
                f"Invalid adapter_type. Must be one of: {valid_adapter_types}",
                adapter_type = adapter_type,
            )

        program_repo = ReferralProgramRepository(db)

        program = program_repo.create(
            name = name,
            program_key = program_key,
            reward_amount = reward_amount,
            reward_currency = reward_currency,
            reward_type = reward_type,
            adapter_type = adapter_type,
            max_rewards_per_user = max_rewards_per_user,
            conversion_window_days = conversion_window_days,
            adapter_config = adapter_config or {},
        )

        return ProgramInfo(
            id = program.id,
            name = program.name,
            program_key = program.program_key,
            reward_amount = program.reward_amount,
            reward_currency = program.reward_currency,
            reward_type = program.reward_type,
            is_active = program.is_active,
        )

    @staticmethod
    def get_program_info(db: Session, program_key: str) -> ProgramInfo:
        """
        Get program information by key
        """
        program_repo = ReferralProgramRepository(db)
        program = program_repo.get_by_key(program_key)

        if not program:
            raise TrackingNotFoundError(
                f"Program '{program_key}' not found",
                program_key = program_key,
            )

        return ProgramInfo(
            id = program.id,
            name = program.name,
            program_key = program.program_key,
            reward_amount = program.reward_amount,
            reward_currency = program.reward_currency,
            reward_type = program.reward_type,
            is_active = program.is_active,
        )

    @staticmethod
    def create_payout(
        db: Session,
        tracking_id: int,
        adapter_type: str,
        recipient_data: dict[str,
                             Any],
    ) -> PayoutInfo:
        """
        Create a payout record for a tracking entry
        """
        tracking_repo = ReferralTrackingRepository(db)
        payout_repo = PayoutRepository(db)
        program_repo = ReferralProgramRepository(db)

        tracking = tracking_repo.get_by_id(tracking_id)
        if not tracking:
            raise TrackingNotFoundError(
                f"Tracking ID {tracking_id} not found",
                tracking_id = tracking_id,
            )

        existing_payout = payout_repo.get_by_tracking_id(tracking_id)
        if existing_payout:
            raise PayoutAlreadyExistsError(
                f"Payout already exists for tracking ID {tracking_id}",
                tracking_id = tracking_id,
            )

        program = program_repo.get_by_id(tracking.program_id)
        if not program:
            raise TrackingNotFoundError(
                f"Program ID {tracking.program_id} not found",
                program_id = tracking.program_id,
            )

        adapter = PayoutService._get_adapter(
            adapter_type,
            program.adapter_config
        )

        validation: RecipientValidation = adapter.validate_recipient(
            recipient_data
        )
        if not validation["valid"]:
            raise InvalidRecipientDataError(
                validation.get("error",
                               "Invalid recipient data"),
                recipient_data = recipient_data,
                adapter_type = adapter_type,
            )

        payout = payout_repo.create(
            user_id = tracking.referrer_user_id,
            tracking_id = tracking_id,
            amount = tracking.amount_earned,
            currency = tracking.currency,
            status = PayoutStatus.PENDING.value,
            adapter_type = adapter_type,
            recipient_data = recipient_data,
        )

        return PayoutInfo(
            id = payout.id,
            user_id = payout.user_id,
            amount = payout.amount,
            currency = payout.currency,
            status = payout.status,
            adapter_type = payout.adapter_type,
            processed_at = payout.processed_at.isoformat()
            if payout.processed_at else None,
            external_transaction_id = payout.external_transaction_id,
        )

    @staticmethod
    def get_payout_info(db: Session, payout_id: int) -> PayoutInfo:
        """
        Get payout information by ID
        """
        payout_repo = PayoutRepository(db)
        payout = payout_repo.get_by_id(payout_id)

        if not payout:
            raise PayoutNotFoundError(
                f"Payout ID {payout_id} not found",
                payout_id = payout_id,
            )

        return PayoutInfo(
            id = payout.id,
            user_id = payout.user_id,
            amount = payout.amount,
            currency = payout.currency,
            status = payout.status,
            adapter_type = payout.adapter_type,
            processed_at = payout.processed_at.isoformat()
            if payout.processed_at else None,
            external_transaction_id = payout.external_transaction_id,
        )

    @staticmethod
    def get_user_payouts(db: Session, user_id: str) -> list[PayoutInfo]:
        """
        Get all payouts for a user
        """
        payout_repo = PayoutRepository(db)
        payouts = payout_repo.get_by_user(user_id)

        return [
            PayoutInfo(
                id = p.id,
                user_id = p.user_id,
                amount = p.amount,
                currency = p.currency,
                status = p.status,
                adapter_type = p.adapter_type,
                processed_at = p.processed_at.isoformat()
                if p.processed_at else None,
                external_transaction_id = p.external_transaction_id,
            ) for p in payouts
        ]

    @staticmethod
    def mark_payout_paid(
        db: Session,
        payout_id: int,
        transaction_id: str,
    ) -> PayoutResult:
        """
        Mark a payout as successfully paid
        """
        payout_repo = PayoutRepository(db)

        payout = payout_repo.mark_as_paid(payout_id, transaction_id)
        if not payout:
            return PayoutResult(
                success = False,
                error = f"Payout ID {payout_id} not found",
            )

        return PayoutResult(
            success = True,
            transaction_id = transaction_id,
        )

    @staticmethod
    def mark_payout_failed(
        db: Session,
        payout_id: int,
        error_message: str,
    ) -> PayoutResult:
        """
        Mark a payout as failed
        """
        payout_repo = PayoutRepository(db)

        payout = payout_repo.mark_as_failed(payout_id, error_message)
        if not payout:
            return PayoutResult(
                success = False,
                error = f"Payout ID {payout_id} not found",
            )

        return PayoutResult(
            success = False,
            error = error_message,
        )
