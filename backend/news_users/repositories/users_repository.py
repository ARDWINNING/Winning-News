from news_backend.db import Database
from uuid import UUID
from news_users.model.user_model import User

class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    # Read Operations
    async def get_user_by_id(self, uuid: UUID) -> User | None:
        query = "SELECT * FROM users WHERE user_id = $1"
        result = await self.db.fetch_one(query, (uuid,))
        return User(**result) if result else None
    
    async def get_user_by_email(self, email: str) -> User | None:
        query = "SELECT * FROM users WHERE email = $1"
        result = await self.db.fetch_one(query, (email,))
        return User(**result) if result else None
    
    # Update Operations
    async def update_user_email(self, user_id: UUID, new_email: str) -> None:
        query = "UPDATE users SET email = $1, updated_at = CURRENT_TIMESTAMP WHERE user_id = $2"
        await self.db.execute(query, (new_email, user_id))
        return
    
    async def update_user_password(self, user_id: UUID, new_password: str, new_salt: str) -> None:
        query = "UPDATE users SET password_hash = $1, password_salt = $2 WHERE user_id = $3"
        await self.db.execute(query, (new_password, new_salt, user_id))
        return
    
    async def update_user_last_login(self, user_id: UUID) -> None:
        query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = $1"
        await self.db.execute(query, (user_id,))
        return
    
    async def update_user_status(self, user_id: UUID, new_status: str) -> None:
        query = "UPDATE users SET status_type = $1 WHERE user_id = $2"
        await self.db.execute(query, (new_status, user_id))
        return
    
    async def update_user_role(self, user_id: UUID, new_role_id: UUID) -> None:
        query = "UPDATE users SET user_role = $1 WHERE user_id = $2"
        await self.db.execute(query, (new_role_id, user_id))
        return
    
    async def update_user_name(self, user_id: UUID, first_name: str, last_name: str) -> None:
        query = "UPDATE users SET first_name = $1, last_name = $2 WHERE user_id = $3"
        await self.db.execute(query, (first_name, last_name, user_id))
        return
    
    # Create Operation
    async def create_user(self, email: str, username: str, first_name: str, last_name: str, pw_hash: str, pw_salt: str, role_id: UUID) -> User:
        query = """
        INSERT INTO users (email, username, first_name, last_name, password_hash, password_salt, user_role)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *;
        """
        result = await self.db.fetch_one(query, (email, username, first_name, last_name, pw_hash, pw_salt, role_id))
        return User(**result) if result else None

    # Soft Delete Operation
    async def delete_user(self, user_id: UUID) -> None:
        query = "UPDATE users SET status_type = 'deleted', deleted_at = CURRENT_TIMESTAMP WHERE user_id = $1"
        await self.db.execute(query, (user_id,))
        return
    
    # Hard Delete Operation
    async def hard_delete_user(self, user_id: UUID) -> None:
        query = "DELETE FROM users WHERE user_id = $1"
        await self.db.execute(query, (user_id,))
        return
    