import asyncpg
from news_backend.db import Database
from news_users.data_classes.permissions_model import Permission, Role, RolePermission
from uuid import UUID

from .queries import (
    GET_PERMISSION_BY_ID,
    GET_ROLE_BY_ID,
    GET_PERMISSIONS_BY_ROLE,
    GET_ROLE_BY_NAME,
    GET_PERMISSION_BY_CODE,
    GET_PERMISSIONS_FOR_USER,
    CREATE_PERMISSION,
    CREATE_ROLE,
    CREATE_ROLE_PERMISSION,
    DELETE_ROLE_PERMISSION,
    DELETE_ROLE_BY_ID,
    DELETE_PERMISSION_BY_ID,
    LIST_ROLES,
    LIST_PERMISSIONS,
)

class Permissions:
    def __init__(self, db: Database):
        self.db = db

    def _to_permission(self, row: dict | None) -> Permission | None:
        return Permission(**row) if row else None
    
    def _to_role(self, row: dict | None) -> Role | None:
        return Role(**row) if row else None
    
    def _to_role_permission(self, row: dict | None) -> RolePermission | None:
        return RolePermission(**row) if row else None

    # Read Operations
    async def get_permission_by_id(self, permission_id: UUID) -> Permission | None:
        record = await self.db.fetch_one(GET_PERMISSION_BY_ID, (permission_id,))
        return self._to_permission(record)
    
    async def get_role_by_id(self, role_id: UUID) -> Role | None:
        record = await self.db.fetch_one(GET_ROLE_BY_ID, (role_id,))
        return self._to_role(record)
    
    async def get_permissions_by_role(self, role_id: UUID) -> list[Permission]:
        records = await self.db.fetch_all(GET_PERMISSIONS_BY_ROLE, (role_id,))
        return [self._to_role_permission(record) for record in records]
    
    async def get_role_by_name(self, role_name: str) -> Role | None:
        record = await self.db.fetch_one(GET_ROLE_BY_NAME, (role_name,))
        return self._to_role(record)
    
    async def get_permission_by_code(self, permission_code: str) -> Permission | None:
        record = await self.db.fetch_one(GET_PERMISSION_BY_CODE, (permission_code,))
        return self._to_permission(record)
    
    async def get_permissions_for_user(self, user_id: UUID) -> list[Permission]:
        records = await self.db.fetch_all(GET_PERMISSIONS_FOR_USER, (user_id,))
        return [self._to_permission(record) for record in records]
    
    # Create Operations
    async def create_permission(self, permission_code: str, description: str) -> Permission:
        record = await self.db.fetch_one(CREATE_PERMISSION, (permission_code, description))
        return self._to_permission(record)
    
    async def create_role(self, role_name: str, description: str) -> Role:
        record = await self.db.fetch_one(CREATE_ROLE, (role_name, description))
        return self._to_role(record)

    async def create_role_permission(self, role_id: UUID, permission_id: UUID) -> RolePermission:
        record = await self.db.fetch_one(CREATE_ROLE_PERMISSION, (role_id, permission_id))
        return self._to_role_permission(record)
    
    # Transactional Create Operations
    async def create_permission_conn(self, connection: asyncpg.Connection, permission_code: str, description: str) -> Permission:
            record = await self.db.fetch_one_conn(connection, CREATE_PERMISSION, (permission_code, description))
            return self._to_permission(record)
    
    async def create_role_conn(self, connection: asyncpg.Connection, role_name: str, description: str) -> Role:
            record = await self.db.fetch_one_conn(connection, CREATE_ROLE, (role_name, description))
            return self._to_role(record)
    
    async def create_role_permission_conn(self, connection: asyncpg.Connection, role_id: UUID, permission_id: UUID) -> RolePermission:
            record = await self.db.fetch_one_conn(connection, CREATE_ROLE_PERMISSION, (role_id, permission_id))
            return self._to_role_permission(record)
    
    # Delete Operations
    async def delete_role_permission(self, role_id: UUID, permission_id: UUID) -> None:
        await self.db.execute(DELETE_ROLE_PERMISSION, (role_id, permission_id))

    async def delete_role_by_id(self, role_id: UUID) -> None:
        await self.db.execute(DELETE_ROLE_BY_ID, (role_id,))

    async def delete_permission_by_id(self, permission_id: UUID) -> None:
        await self.db.execute(DELETE_PERMISSION_BY_ID, (permission_id,))

    # Pagination Operations
    async def list_roles(self) -> list[Role]:
        records = await self.db.fetch_all(LIST_ROLES)
        return [self._to_role(record) for record in records]
    
    async def list_permissions(self) -> list[Permission]:
        records = await self.db.fetch_all(LIST_PERMISSIONS)
        return [self._to_permission(record) for record in records]