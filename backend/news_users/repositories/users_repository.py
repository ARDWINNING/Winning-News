import asyncpg
from news_backend.db import Database
from uuid import UUID
from news_users.model.user_model import User

from .queries import (
    GET_USER_BY_ID,
    GET_USER_BY_EMAIL,
    UPDATE_EMAIL,
    UPDATE_PASSWORD,
    UPDATE_LAST_LOGIN,
    UPDATE_STATUS,
    UPDATE_ROLE,
    UPDATE_NAME,
    CREATE_USER,
    SOFT_DELETE,
    HARD_DELETE,
    LIST_USERS,
    LIST_USERS_ROLE,
    COUNT_USERS
)

class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def _to_user(self, row: dict | None) -> User | None:
        return User(**row) if row else None

    # Read Operations
    async def get_user_by_id(self, uuid: UUID) -> User | None:
        result = await self.db.fetch_one(GET_USER_BY_ID, (uuid,))
        return self._to_user(result)
    
    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.fetch_one(GET_USER_BY_EMAIL, (email,))
        return self._to_user(result)
    
    # Update Operations
    async def update_user_email(self, user_id: UUID, new_email: str) -> None:
        await self.db.execute(UPDATE_EMAIL, (new_email, user_id))
    
    async def update_user_password(self, user_id: UUID, new_password: bytes, new_salt: bytes) -> None:
        await self.db.execute(UPDATE_PASSWORD, (new_password, new_salt, user_id))
    
    async def update_user_last_login(self, user_id: UUID) -> None:
        await self.db.execute(UPDATE_LAST_LOGIN, (user_id,))

    async def update_user_status(self, user_id: UUID, new_status: str) -> None:
        await self.db.execute(UPDATE_STATUS, (new_status, user_id))
    
    async def update_user_role(self, user_id: UUID, new_role_id: UUID) -> None:
        await self.db.execute(UPDATE_ROLE, (new_role_id, user_id))

    async def update_user_name(self, user_id: UUID, first_name: str, last_name: str) -> None:
        await self.db.execute(UPDATE_NAME, (first_name, last_name, user_id))
    
    # Transactional Update Operations
    async def update_user_email_conn(self, connection: asyncpg.Connection, user_id: UUID, new_email: str) -> None:
        await self.db.execute_conn(connection, UPDATE_EMAIL, (new_email, user_id))

    async def update_user_password_conn(self, connection: asyncpg.Connection, user_id: UUID, new_password: bytes, new_salt: bytes) -> None:
        await self.db.execute_conn(connection, UPDATE_PASSWORD, (new_password, new_salt, user_id))
    
    async def update_user_last_login_conn(self, connection: asyncpg.Connection, user_id: UUID) -> None:
        await self.db.execute_conn(connection, UPDATE_LAST_LOGIN, (user_id,))
    
    async def update_user_status_conn(self, connection: asyncpg.Connection, user_id: UUID, new_status: str) -> None:
        await self.db.execute_conn(connection, UPDATE_STATUS, (new_status, user_id))
    
    async def update_user_role_conn(self, connection: asyncpg.Connection, user_id: UUID, new_role_id: UUID) -> None:
        await self.db.execute_conn(connection, UPDATE_ROLE, (new_role_id, user_id))
    
    async def update_user_name_conn(self, connection: asyncpg.Connection, user_id: UUID, first_name: str, last_name: str) -> None:
        await self.db.execute_conn(connection, UPDATE_NAME, (first_name, last_name, user_id))

    # Create Operation
    async def create_user(self, email: str, username: str, first_name: str, last_name: str, pw_hash: bytes, pw_salt: bytes, role_id: UUID) -> User:
        result = await self.db.fetch_one(CREATE_USER, (email, username, first_name, last_name, pw_hash, pw_salt, role_id))
        return self._to_user(result)

    # Transactional Create Operation
    async def create_user_conn(self, connection: asyncpg.Connection, email: str, username: str, first_name: str, last_name: str, pw_hash: bytes, pw_salt: bytes, role_id: UUID) -> User:
        result = await self.db.fetch_one_conn(connection, CREATE_USER, (email, username, first_name, last_name, pw_hash, pw_salt, role_id))
        return self._to_user(result)

    # Soft Delete Operation
    async def delete_user(self, user_id: UUID) -> None:
        await self.db.execute(SOFT_DELETE, (user_id,))
    
    # Transactional Soft Delete Operation
    async def delete_user_conn(self, connection: asyncpg.Connection, user_id: UUID) -> None:
        await self.db.execute_conn(connection, SOFT_DELETE, (user_id,))
    
    # Hard Delete Operation
    async def hard_delete_user(self, user_id: UUID) -> None:
        await self.db.execute(HARD_DELETE, (user_id,))
    
    # Transactional Hard Delete Operation
    async def hard_delete_user_conn(self, connection: asyncpg.Connection, user_id: UUID) -> None:
        await self.db.execute_conn(connection, HARD_DELETE, (user_id,))
    
    # Pagination Operation
    async def list_users(self, limit: int, offset: int) -> list[User]:
        results = await self.db.fetch_all(LIST_USERS, (limit, offset))
        return [self._to_user(row) for row in results]
    
    async def list_users_by_role(self, role_id: UUID, limit: int, offset: int) -> list[User]:
        results = await self.db.fetch_all(LIST_USERS_ROLE, (role_id, limit, offset))
        return [self._to_user(row) for row in results]
    
    async def count_users(self) -> int:
        result = await self.db.fetch_value(COUNT_USERS)
        return int(result) if result else 0
    
    # May need transactional versions of pagination and count methods
    # May need the count to be accurate within a transaction for metadata purposes