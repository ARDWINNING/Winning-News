# SQL Queries for User Repository
GET_USER_BY_ID = "SELECT * FROM users WHERE user_id = $1"
GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = $1"
UPDATE_EMAIL = "UPDATE users SET email = $1 WHERE user_id = $2"
UPDATE_PASSWORD = "UPDATE users SET password_hash = $1, password_salt = $2 WHERE user_id = $3"
UPDATE_LAST_LOGIN = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = $1"
UPDATE_STATUS = "UPDATE users SET status_type = $1 WHERE user_id = $2"
UPDATE_ROLE = "UPDATE users SET user_role = $1 WHERE user_id = $2"
UPDATE_NAME = "UPDATE users SET first_name = $1, last_name = $2 WHERE user_id = $3"
CREATE_USER = """
        INSERT INTO users (email, username, first_name, last_name, password_hash, password_salt, user_role)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *;
        """
SOFT_DELETE_USER_BY_ID = "UPDATE users SET status_type = 'deleted', deleted_at = CURRENT_TIMESTAMP WHERE user_id = $1"
HARD_DELETE_USER_BY_ID = "DELETE FROM users WHERE user_id = $1"
LIST_USERS = "SELECT * FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2"
LIST_USERS_ROLE = "SELECT * FROM users WHERE user_role = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3"
COUNT_USERS = "SELECT COUNT(*) AS count FROM users"

# SQL Queries for Session Repository
GET_SESSION_BY_ID = "SELECT * FROM sessions WHERE session_id = $1"
GET_SESSION_BY_USER = "SELECT * FROM sessions WHERE user_id = $1"
GET_SESSION_BY_HASH = "SELECT * FROM sessions WHERE token_hash = $1"
CREATE_SESSION = """
        INSERT INTO sessions (user_id, token_hash, expires_at)
        VALUES ($1, $2, $3)
        RETURNING *;
        """
DELETE_SESSION_BY_ID = "DELETE FROM sessions WHERE session_id = $1"
LIST_EXPIRED_SESSIONS = "SELECT * FROM sessions WHERE expires_at < CURRENT_TIMESTAMP"