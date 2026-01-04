
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
SOFT_DELETE = "UPDATE users SET status_type = 'deleted', deleted_at = CURRENT_TIMESTAMP WHERE user_id = $1"
HARD_DELETE = "DELETE FROM users WHERE user_id = $1"
    