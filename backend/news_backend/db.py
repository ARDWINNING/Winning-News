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

    async def fetch_one(self, sql: str, params: tuple | None = None) -> dict | None:
        self.safe()
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(sql, *params) if params else await connection.fetchrow(sql)
            return dict(row) if row else None 

    async def fetch_all(self, sql: str, params: tuple | None = None) -> list[dict]:
        self.safe()
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(sql, *params) if params else await connection.fetch(sql)
            return [dict(row) for row in rows]
    
    async def execute(self, sql: str, params: tuple | None = None) -> str:
        self.safe()
        async with self.pool.acquire() as connection:
            result = await connection.execute(sql, *params) if params else await connection.execute(sql)
            return result