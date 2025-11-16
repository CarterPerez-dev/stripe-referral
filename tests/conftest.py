"""
ⒸAngelaMos | 2025 | CertGames.com
Pytest configuration and fixtures
"""

import sys
from datetime import (
    UTC,
    datetime,
)
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from stripe_referral.database.Base import Base
from stripe_referral.models.Payout import Payout
from stripe_referral.models.ReferralCode import ReferralCode
from stripe_referral.models.ReferralProgram import ReferralProgram
from stripe_referral.models.ReferralTracking import ReferralTracking


@pytest.fixture(scope = "function")
def db_session() -> Session:
    """
    Create an in-memory SQLite database for testing
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind = engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_program(db_session: Session) -> ReferralProgram:
    """
    Create a sample referral program for testing
    """
    program = ReferralProgram(
        name = "Test Program",
        program_key = "test_program",
        reward_amount = 50.0,
        reward_currency = "USD",
        reward_type = "one_time",
        is_active = True,
        adapter_type = "manual",
        adapter_config = {},
    )
    db_session.add(program)
    db_session.commit()
    db_session.refresh(program)
    return program


@pytest.fixture
def sample_code(
    db_session: Session,
    sample_program: ReferralProgram
) -> ReferralCode:
    """
    Create a sample referral code for testing
    """
    code = ReferralCode(
        code = "TEST_ABC_xyz123",
        user_id = "user_123",
        program_id = sample_program.id,
        status = "active",
        uses_count = 0,
        max_uses = None,
        expires_at = None,
    )
    db_session.add(code)
    db_session.commit()
    db_session.refresh(code)
    return code


@pytest.fixture
def sample_tracking(
    db_session: Session,
    sample_program: ReferralProgram,
    sample_code: ReferralCode
) -> ReferralTracking:
    """
    Create a sample referral tracking for testing
    """
    tracking = ReferralTracking(
        referrer_user_id = "user_123",
        referred_user_id = "user_456",
        code_id = sample_code.id,
        program_id = sample_program.id,
        transaction_id = "txn_test123",
        transaction_amount = 100.0,
        amount_earned = 50.0,
        currency = "USD",
        converted_at = datetime.now(UTC),
        payout_status = "pending",
    )
    db_session.add(tracking)
    db_session.commit()
    db_session.refresh(tracking)
    return tracking


@pytest.fixture
def sample_payout(
    db_session: Session,
    sample_tracking: ReferralTracking
) -> Payout:
    """
    Create a sample payout for testing
    """
    payout = Payout(
        user_id = "user_123",
        tracking_id = sample_tracking.id,
        amount = 50.0,
        currency = "USD",
        status = "pending",
        adapter_type = "manual",
        recipient_data = {
            "bank_account_number": "123456789",
            "routing_number": "987654321",
            "account_holder_name": "Test User",
        },
    )
    db_session.add(payout)
    db_session.commit()
    db_session.refresh(payout)
    return payout
