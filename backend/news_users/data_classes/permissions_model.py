from dataclasses import dataclass
from uuid import UUID

@dataclass
class Permission:
    permission_id: UUID
    permission_code: str
    description: str

@dataclass
class Role:
    role_id: UUID
    role_name: str
    description: str

@dataclass
class RolePermission:
    role_id: UUID
    permission_id: UUID