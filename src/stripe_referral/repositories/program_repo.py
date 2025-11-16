"""
ⒸAngelaMos | 2025 | CertGames.com
Referral program repository
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.ReferralProgram import ReferralProgram

from .base import BaseRepository


class ReferralProgramRepository(BaseRepository[ReferralProgram]):
    """
    Repository for ReferralProgram database operations
    """
    def __init__(self, db: Session) -> None:
        """
        Initialize with ReferralProgram model
        """
        super().__init__(db, ReferralProgram)

    def get_by_key(self, program_key: str) -> ReferralProgram | None:
        """
        Get program by unique program key
        """
        stmt = select(ReferralProgram).where(
            ReferralProgram.program_key == program_key
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_name(self, name: str) -> ReferralProgram | None:
        """
        Get program by unique name
        """
        stmt = select(ReferralProgram).where(ReferralProgram.name == name)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_active_programs(self) -> list[ReferralProgram]:
        """
        Get all active programs
        """
        stmt = select(ReferralProgram).where(ReferralProgram.is_active)
        return list(self.db.execute(stmt).scalars().all())

    def deactivate_program(
        self,
        program_id: int
    ) -> ReferralProgram | None:
        """
        Deactivate a program
        """
        program = self.get_by_id(program_id)
        if not program:
            return None

        program.is_active = False
        self.db.commit()
        self.db.refresh(program)
        return program

    def activate_program(self, program_id: int) -> ReferralProgram | None:
        """
        Activate a program
        """
        program = self.get_by_id(program_id)
        if not program:
            return None

        program.is_active = True
        self.db.commit()
        self.db.refresh(program)
        return program
