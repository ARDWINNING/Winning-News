from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class Session:
    session_id: UUID
    user_id: UUID
    token_hash: bytes
    created_at: datetime
    expires_at: datetime