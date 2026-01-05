import asyncpg
from news_backend.db import Database
from news_users.data_classes.session_model import Session
from datetime import datetime
from uuid import UUID

from .queries import (
    GET_SESSION_BY_ID,
    GET_SESSION_BY_USER,
    GET_SESSION_BY_HASH,
    CREATE_SESSION,
    DELETE_SESSION_BY_ID,
    LIST_EXPIRED_SESSIONS,
)

class SessionsRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def _to_session(self, row: dict | None) -> Session | None:
        return Session(**row) if row else None

    # Read Operations
    async def get_session_by_id(self, session_id: UUID) -> Session | None:
        result = await self.db.fetch_one(GET_SESSION_BY_ID, (session_id,))
        return self._to_session(result)
    
    async def get_session_by_user(self, user_id: UUID) -> Session | None:
        result = await self.db.fetch_one(GET_SESSION_BY_USER, (user_id,))
        return self._to_session(result)
    
    async def get_session_by_hash(self, token_hash: bytes) -> Session | None:
        result = await self.db.fetch_one(GET_SESSION_BY_HASH, (token_hash,))
        return self._to_session(result)
    
    # Create Operation
    async def create_session(self, user_id: UUID, token_hash: bytes, expires_at: datetime) -> Session:
        result = await self.db.fetch_one(CREATE_SESSION, (user_id, token_hash, expires_at))
        return self._to_session(result)
    
    # Transactional Create Operation
    async def create_session_conn(self, connection: asyncpg.Connection, user_id: UUID, token_hash: bytes, expires_at: datetime) -> Session:
        result = await self.db.fetch_one_conn(connection, CREATE_SESSION, (user_id, token_hash, expires_at))
        return self._to_session(result)
    
    # Delete Operation
    async def delete_session_by_id(self, session_id: UUID) -> None:
        await self.db.execute(DELETE_SESSION_BY_ID, (session_id,))

    # Transactional Delete Operation
    async def delete_session_by_id_conn(self, connection: asyncpg.Connection, session_id: UUID) -> None:
        await self.db.execute_conn(connection, DELETE_SESSION_BY_ID, (session_id,))

    # List Operation
    async def list_expired_sessions(self) -> list[Session]:
        rows = await self.db.fetch_all(LIST_EXPIRED_SESSIONS)
        return [self._to_session(row) for row in rows]
    
    # Transactional List Operation
    async def list_expired_sessions_conn(self, connection: asyncpg.Connection) -> list[Session]:
        rows = await self.db.fetch_all_conn(connection, LIST_EXPIRED_SESSIONS)
        return [self._to_session(row) for row in rows]

    