"""
ⒸAngelaMos | 2025 | CertGames.com
Referral code generation utilities
"""

import hashlib
import secrets

from ..config.constants import (
    CODE_LENGTH,
    CODE_PREFIX,
    CODE_SEPARATOR,
    CODE_GENERATION_RETRY_ATTEMPTS,
)
from ..exceptions.errors import CodeGenerationError


def _generate_code_string(user_id: str, program_key: str) -> str:
    """
    Internal function to generate a single code string
    """
    random_part = secrets.token_urlsafe(CODE_LENGTH)[: CODE_LENGTH]

    hash_input = f"{user_id}:{program_key}:{random_part}"
    hash_part = hashlib.sha256(hash_input.encode()
                               ).hexdigest()[: 6].upper()

    return f"{CODE_PREFIX}{CODE_SEPARATOR}{hash_part}{CODE_SEPARATOR}{random_part}"


def generate_unique_code(
    user_id: str,
    program_key: str,
    check_collision_fn
) -> str:
    """
    Generate unique referral code with collision detection

    Args:
        user_id: User identifier
        program_key: Program key
        check_collision_fn: Function that takes 
        a code string and returns True if collision

    Returns:
        Unique referral code

    Raises:
        CodeGenerationError: If unable to
        generate unique code after max attempts
    """
    for _attempt in range(CODE_GENERATION_RETRY_ATTEMPTS):
        code = _generate_code_string(user_id, program_key)

        if not check_collision_fn(code):
            return code

    raise CodeGenerationError(
        f"Failed to generate unique code after {CODE_GENERATION_RETRY_ATTEMPTS} attempts",
        user_id = user_id,
        program_key = program_key,
        attempts = CODE_GENERATION_RETRY_ATTEMPTS,
    )
