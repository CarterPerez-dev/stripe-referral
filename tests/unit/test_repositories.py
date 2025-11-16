"""
ⒸAngelaMos | 2025 | CertGames.com
Unit tests for repository layer
"""

from sqlalchemy.orm import Session

from src.stripe_referral.models.ReferralCode import ReferralCode
from src.stripe_referral.models.ReferralProgram import ReferralProgram
from src.stripe_referral.models.ReferralTracking import ReferralTracking
from src.stripe_referral.repositories.payout_repo import PayoutRepository
from src.stripe_referral.repositories.program_repo import (
    ReferralProgramRepository,
)
from src.stripe_referral.repositories.referral_repo import (
    ReferralCodeRepository,
    ReferralTrackingRepository,
)


class TestReferralProgramRepository:
    """
    Test ReferralProgramRepository
    """
    def test_create_program(self, db_session: Session) -> None:
        """
        Test creating a referral program
        """
        repo = ReferralProgramRepository(db_session)

        program = repo.create(
            name = "Test Program",
            program_key = "test_key",
            reward_amount = 100.0,
            reward_currency = "USD",
            reward_type = "one_time",
            is_active = True,
            adapter_type = "manual",
        )

        assert program.id is not None
        assert program.name == "Test Program"
        assert program.program_key == "test_key"
        assert program.reward_amount == 100.0
        assert program.is_active is True

    def test_get_by_key(
        self,
        db_session: Session,
        sample_program: ReferralProgram
    ) -> None:
        """
        Test getting program by key
        """
        repo = ReferralProgramRepository(db_session)

        program = repo.get_by_key("test_program")

        assert program is not None
        assert program.id == sample_program.id
        assert program.program_key == "test_program"

    def test_get_active_programs(
        self,
        db_session: Session,
        sample_program: ReferralProgram
    ) -> None:
        """
        Test getting only active programs
        """
        repo = ReferralProgramRepository(db_session)

        inactive_program = repo.create(
            name = "Inactive Program",
            program_key = "inactive",
            reward_amount = 50.0,
            is_active = False,
        )

        active_programs = repo.get_active_programs()

        assert len(active_programs) == 1
        assert active_programs[0].id == sample_program.id
        assert inactive_program.id not in [p.id for p in active_programs]


class TestReferralCodeRepository:
    """
    Test ReferralCodeRepository
    """
    def test_get_by_code(
        self,
        db_session: Session,
        sample_code: ReferralCode
    ) -> None:
        """
        Test getting code by code string
        """
        repo = ReferralCodeRepository(db_session)

        code = repo.get_by_code("TEST_ABC_xyz123")

        assert code is not None
        assert code.id == sample_code.id
        assert code.code == "TEST_ABC_xyz123"

    def test_get_by_user(
        self,
        db_session: Session,
        sample_code: ReferralCode,
        sample_program: ReferralProgram
    ) -> None:
        """
        Test getting codes by user ID
        """
        repo = ReferralCodeRepository(db_session)

        codes = repo.get_by_user("user_123")

        assert len(codes) == 1
        assert codes[0].id == sample_code.id

    def test_increment_uses(
        self,
        db_session: Session,
        sample_code: ReferralCode
    ) -> None:
        """
        Test incrementing code usage count
        """
        repo = ReferralCodeRepository(db_session)

        initial_count = sample_code.uses_count
        success = repo.increment_uses(sample_code.id)

        assert success is True

        db_session.refresh(sample_code)
        assert sample_code.uses_count == initial_count + 1


class TestReferralTrackingRepository:
    """
    Test ReferralTrackingRepository
    """
    def test_get_by_referrer(
        self,
        db_session: Session,
        sample_tracking: ReferralTracking
    ) -> None:
        """
        Test getting trackings by referrer user ID
        """
        repo = ReferralTrackingRepository(db_session)

        trackings = repo.get_by_referrer("user_123")

        assert len(trackings) == 1
        assert trackings[0].id == sample_tracking.id
        assert trackings[0].referrer_user_id == "user_123"

    def test_get_user_earnings(
        self,
        db_session: Session,
        sample_tracking: ReferralTracking
    ) -> None:
        """
        Test calculating user earnings
        """
        repo = ReferralTrackingRepository(db_session)

        earnings = repo.get_user_earnings("user_123")

        assert earnings["total"] == 50.0
        assert earnings["pending"] == 50.0
        assert earnings["paid"] == 0.0


class TestPayoutRepository:
    """
    Test PayoutRepository
    """
    def test_get_by_tracking_id(
        self,
        db_session: Session,
        sample_payout
    ) -> None:
        """
        Test getting payout by tracking ID
        """
        repo = PayoutRepository(db_session)

        payout = repo.get_by_tracking_id(sample_payout.tracking_id)

        assert payout is not None
        assert payout.id == sample_payout.id

    def test_mark_as_paid(
        self,
        db_session: Session,
        sample_payout
    ) -> None:
        """
        Test marking payout as paid
        """
        repo = PayoutRepository(db_session)

        updated = repo.mark_as_paid(
            sample_payout.id,
            "external_txn_123"
        )

        assert updated is not None
        assert updated.status == "paid"
        assert updated.external_transaction_id == "external_txn_123"
        assert updated.processed_at is not None
