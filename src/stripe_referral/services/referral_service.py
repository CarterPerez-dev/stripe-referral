"""
ⒸAngelaMos | 2025 | CertGames.com
Referral service with business logic
"""

from datetime import UTC, datetime
from sqlalchemy.orm import Session

from ..config.enums import ReferralCodeStatus
from ..exceptions.errors import (
    CodeExpiredError,
    CodeInactiveError,
    CodeMaxUsesReachedError,
    CodeNotFoundError,
    ProgramNotFoundError,
    SelfReferralError,
)
from ..repositories.referral_repo import (
    ReferralCodeRepository,
    ReferralTrackingRepository,
)
from ..repositories.program_repo import (
    ReferralProgramRepository,
)
from ..schemas.types import (
    CodeValidation,
    CreateCodeResult,
    ReferralHistoryItem,
    TrackReferralResult,
    UserEarnings,
)
from ..utils.code_generator import generate_unique_code


class ReferralService:
    """
    Service for referral business logic
    """
    @staticmethod
    def create_code(
        db: Session,
        user_id: str,
        program_key: str
    ) -> CreateCodeResult:
        """
        Generate unique referral code for a user
        """
        program_repo = ReferralProgramRepository(db)
        code_repo = ReferralCodeRepository(db)

        program = program_repo.get_by_key(program_key)
        if not program or not program.is_active:
            raise ProgramNotFoundError(
                f"Program '{program_key}' not found or inactive",
                program_key = program_key,
            )

        def check_collision(code_string: str) -> bool:
            """
            Check if code already exists in database
            """
            existing = code_repo.get_by_code(code_string)
            return existing is not None

        unique_code = generate_unique_code(
            user_id,
            program_key,
            check_collision
        )

        code = code_repo.create(
            code = unique_code,
            user_id = user_id,
            program_id = program.id,
            status = ReferralCodeStatus.ACTIVE.value,
        )

        return CreateCodeResult(
            code = code.code,
            program_id = code.program_id,
            user_id = code.user_id,
            created_at = code.created_at.isoformat(),
        )

    @staticmethod
    def validate_code(db: Session, code: str) -> CodeValidation:
        """
        Validate if a code is active and usable
        """
        code_repo = ReferralCodeRepository(db)

        code_obj = code_repo.get_by_code(code)
        if not code_obj:
            raise CodeNotFoundError(
                f"Code '{code}' not found",
                code = code
            )

        if code_obj.status != ReferralCodeStatus.ACTIVE.value:
            raise CodeInactiveError(
                f"Code '{code}' is inactive (status: {code_obj.status})",
                code = code,
                status = code_obj.status,
            )

        if code_obj.expires_at and code_obj.expires_at < datetime.now(UTC
                                                                      ):
            raise CodeExpiredError(
                f"Code '{code}' expired at {code_obj.expires_at.isoformat()}",
                code = code,
                expires_at = code_obj.expires_at.isoformat(),
            )

        if code_obj.max_uses and code_obj.uses_count >= code_obj.max_uses:
            raise CodeMaxUsesReachedError(
                f"Code '{code}' has reached maximum uses ({code_obj.max_uses})",
                code = code,
                max_uses = code_obj.max_uses,
                uses_count = code_obj.uses_count,
            )

        return CodeValidation(
            valid = True,
            code_id = code_obj.id,
            program_id = code_obj.program_id,
            referrer_user_id = code_obj.user_id,
        )

    @staticmethod
    def track_referral(
        db: Session,
        code: str,
        referred_user_id: str,
        transaction_id: str | None = None,
        transaction_amount: float | None = None,
    ) -> TrackReferralResult:
        """
        Track a successful referral conversion
        """
        code_repo = ReferralCodeRepository(db)
        tracking_repo = ReferralTrackingRepository(db)
        program_repo = ReferralProgramRepository(db)

        ReferralService.validate_code(db, code)

        code_obj = code_repo.get_by_code(code)
        if not code_obj:
            raise CodeNotFoundError(
                f"Code '{code}' not found",
                code = code
            )

        if code_obj.user_id == referred_user_id:
            raise SelfReferralError(
                "Cannot use your own referral code",
                user_id = referred_user_id,
            )

        program = program_repo.get_by_id(code_obj.program_id)
        if not program:
            raise ProgramNotFoundError(
                f"Program ID {code_obj.program_id} not found",
                program_id = code_obj.program_id,
            )

        tracking = tracking_repo.create(
            referrer_user_id = code_obj.user_id,
            referred_user_id = referred_user_id,
            code_id = code_obj.id,
            program_id = program.id,
            transaction_id = transaction_id,
            transaction_amount = transaction_amount,
            amount_earned = program.reward_amount,
            currency = program.reward_currency,
        )

        code_repo.increment_uses(code_obj.id)

        return TrackReferralResult(
            tracking_id = tracking.id,
            referrer_user_id = tracking.referrer_user_id,
            referred_user_id = tracking.referred_user_id,
            amount_earned = tracking.amount_earned,
            currency = tracking.currency,
            converted_at = tracking.converted_at.isoformat(),
        )

    @staticmethod
    def get_user_earnings(db: Session, user_id: str) -> UserEarnings:
        """
        Get earnings breakdown for a user
        """
        tracking_repo = ReferralTrackingRepository(db)
        earnings_dict = tracking_repo.get_user_earnings(user_id)

        return UserEarnings(
            total = earnings_dict["total"],
            pending = earnings_dict["pending"],
            paid = earnings_dict["paid"],
        )

    @staticmethod
    def get_referral_history(db: Session,
                             user_id: str) -> list[ReferralHistoryItem]:
        """
        Get all referral conversions for a user
        """
        tracking_repo = ReferralTrackingRepository(db)
        trackings = tracking_repo.get_by_referrer(user_id)

        return [
            ReferralHistoryItem(
                referred_user_id = t.referred_user_id,
                amount_earned = t.amount_earned,
                currency = t.currency,
                converted_at = t.converted_at.isoformat(),
                payout_status = t.payout_status,
            ) for t in trackings
        ]
