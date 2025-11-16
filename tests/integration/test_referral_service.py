"""
ⒸAngelaMos | 2025 | CertGames.com
Integration tests for ReferralService
"""

import pytest
from sqlalchemy.orm import Session

from src.stripe_referral.exceptions.errors import (
    CodeExpiredError,
    CodeInactiveError,
    CodeNotFoundError,
    ProgramNotFoundError,
    SelfReferralError,
)
from src.stripe_referral.models.ReferralProgram import (
    ReferralProgram,
)
from src.stripe_referral.services.referral_service import (
    ReferralService,
)


class TestReferralServiceCreateCode:
    """
    Test ReferralService.create_code()
    """
    def test_create_code_success(
        self,
        db_session: Session,
        sample_program: ReferralProgram
    ) -> None:
        """
        Test creating a referral code successfully
        """
        result = ReferralService.create_code(
            db = db_session,
            user_id = "user_789",
            program_key = "test_program",
        )

        assert result["code"] is not None
        assert result["program_id"] == sample_program.id
        assert result["user_id"] == "user_789"
        assert "created_at" in result

    def test_create_code_program_not_found(
        self,
        db_session: Session
    ) -> None:
        """
        Test creating code with non-existent program
        """
        with pytest.raises(ProgramNotFoundError):
            ReferralService.create_code(
                db = db_session,
                user_id = "user_789",
                program_key = "nonexistent",
            )


class TestReferralServiceValidateCode:
    """
    Test ReferralService.validate_code()
    """
    def test_validate_code_success(
        self,
        db_session: Session,
        sample_code
    ) -> None:
        """
        Test validating an active code
        """
        result = ReferralService.validate_code(
            db = db_session,
            code = "TEST_ABC_xyz123",
        )

        assert result["valid"] is True
        assert result["code_id"] == sample_code.id
        assert result["referrer_user_id"] == "user_123"

    def test_validate_code_not_found(self, db_session: Session) -> None:
        """
        Test validating non-existent code
        """
        with pytest.raises(CodeNotFoundError):
            ReferralService.validate_code(
                db = db_session,
                code = "INVALID_CODE",
            )

    def test_validate_code_inactive(
        self,
        db_session: Session,
        sample_code
    ) -> None:
        """
        Test validating inactive code
        """
        sample_code.status = "inactive"
        db_session.commit()

        with pytest.raises(CodeInactiveError):
            ReferralService.validate_code(
                db = db_session,
                code = "TEST_ABC_xyz123",
            )


class TestReferralServiceTrackReferral:
    """
    Test ReferralService.track_referral()
    """
    def test_track_referral_success(
        self,
        db_session: Session,
        sample_code
    ) -> None:
        """
        Test tracking a referral conversion
        """
        result = ReferralService.track_referral(
            db = db_session,
            code = "TEST_ABC_xyz123",
            referred_user_id = "user_new",
            transaction_id = "txn_abc123",
            transaction_amount = 100.0,
        )

        assert result["tracking_id"] is not None
        assert result["referrer_user_id"] == "user_123"
        assert result["referred_user_id"] == "user_new"
        assert result["amount_earned"] == 50.0

    def test_track_referral_self_referral(
        self,
        db_session: Session,
        sample_code
    ) -> None:
        """
        Test preventing self-referral
        """
        with pytest.raises(SelfReferralError):
            ReferralService.track_referral(
                db = db_session,
                code = "TEST_ABC_xyz123",
                referred_user_id = "user_123",
            )


class TestReferralServiceEarnings:
    """
    Test ReferralService earnings methods
    """
    def test_get_user_earnings(
        self,
        db_session: Session,
        sample_tracking
    ) -> None:
        """
        Test getting user earnings
        """
        earnings = ReferralService.get_user_earnings(
            db = db_session,
            user_id = "user_123",
        )

        assert earnings["total"] == 50.0
        assert earnings["pending"] == 50.0
        assert earnings["paid"] == 0.0

    def test_get_referral_history(
        self,
        db_session: Session,
        sample_tracking
    ) -> None:
        """
        Test getting referral history
        """
        history = ReferralService.get_referral_history(
            db = db_session,
            user_id = "user_123",
        )

        assert len(history) == 1
        assert history[0]["referred_user_id"] == "user_456"
        assert history[0]["amount_earned"] == 50.0
