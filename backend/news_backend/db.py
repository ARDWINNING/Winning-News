from uuid import UUID
from contextlib import asynccontextmanager
import asyncpg
from settings import DB_DSN

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        if(self.pool is None):
            self.pool = await asyncpg.create_pool(
                dsn=DB_DSN, min_size=2, 
                max_size=10, command_timeout=60 # Initial connection pool settings
            )
    def safe(self) -> None:
        if self.pool is None:
            raise RuntimeError("Database connection is not established.")
    
    async def disconnect(self):
        if(self.pool):
            await self.pool.close()
            self.pool = None

    @asynccontextmanager
    async def transaction(self):
        connection = await self.pool.acquire()
        try:
            tx = connection.transaction()
            await tx.start()
            yield connection
            await tx.commit()
        except:
            await tx.rollback()
            raise
        finally:
            await self.pool.release(connection)
    
    # Non-transactional Operations
    async def fetch_value(self, sql: str, params: tuple | None = None) -> str | int | bool | UUID | bytes | None:
        self.safe()
        params = params or ()
        async with self.pool.acquire() as connection:
            return await connection.fetchval(sql, *params)

    async def fetch_one(self, sql: str, params: tuple | None = None) -> dict | None:
        self.safe()
        params = params or ()
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(sql, *params)
            return dict(row) if row else None

    async def fetch_all(self, sql: str, params: tuple | None = None) -> list[dict]:
        self.safe()
        params = params or ()
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(sql, *params)
            return [dict(r) for r in rows]
    
    async def execute(self, sql: str, params: tuple | None = None) -> str:
        self.safe()
        params = params or ()
        async with self.pool.acquire() as connection:
            return await connection.execute(sql, *params)
        
    # Transactional Operations
    async def fetch_value_conn(self, connection: asyncpg.Connection, sql: str, params: tuple | None = None) -> str | int | bool | UUID | bytes | None:
        params = params or ()
        return await connection.fetchval(sql, *params)
    
    async def fetch_one_conn(self, connection: asyncpg.Connection, sql: str, params: tuple | None = None) -> dict | None:
        params = params or ()
        row = await connection.fetchrow(sql, *params)
        return dict(row) if row else None
    
    async def fetch_all_conn(self, connection: asyncpg.Connection, sql: str, params: tuple | None = None) -> list[dict]:
        params = params or ()
        rows = await connection.fetch(sql, *params)
        return [dict(r) for r in rows]
    
    async def execute_conn(self, connection: asyncpg.Connection, sql: str, params: tuple | None = None) -> str:
        params = params or ()
        return await connection.execute(sql, *params)