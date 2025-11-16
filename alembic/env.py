"""
ⒸAngelaMos | 2025 | CertGames.com
"""

from sqlalchemy import (
    pool,
    engine_from_config,
)
from alembic import context
from logging.config import fileConfig

from src.stripe_referral.database.Base import Base
from src.stripe_referral.models.Payout import Payout
from src.stripe_referral.config.settings import settings
from src.stripe_referral.models.ReferralCode import ReferralCode
from src.stripe_referral.models.ReferralProgram import ReferralProgram
from src.stripe_referral.models.ReferralTracking import ReferralTracking

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
