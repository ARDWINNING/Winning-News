from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class User:
    user_id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    password_hash: bytes
    password_salt: bytes
    user_role: UUID
    status_type: str
    created_at: datetime
    updated_at: datetime | None
    last_login: datetime | None
    deleted_at: datetime | None
