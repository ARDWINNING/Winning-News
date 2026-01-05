# SQL Queries for User Repository
GET_USER_BY_ID = "SELECT * FROM users WHERE user_id = $1"
GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = $1"
GET_USER_BY_USERNAME = "SELECT * FROM users WHERE username = $1"
UPDATE_EMAIL = "UPDATE users SET email = $1 WHERE user_id = $2"
UPDATE_USERNAME = "UPDATE users SET username = $1 WHERE user_id = $2"
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
LIST_USERS_BY_STATUS = "SELECT * FROM users WHERE status_type = $1 LIMIT $2 OFFSET $3"
COUNT_USERS = "SELECT COUNT(*) AS count FROM users"
COUNT_USERS_BY_ROLE = "SELECT COUNT(*) FROM users WHERE user_role = $1"
SEARCH_USERS = "SELECT * FROM users WHERE email ILIKE $1 OR username ILIKE $1 LIMIT $2 OFFSET $3"

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
DELETE_SESSIONS_BY_USER = "DELETE FROM user_sessions WHERE user_id = $1"
DELETE_EXPIRED_SESSIONS = "DELETE FROM user_sessions WHERE expires_at < CURRENT_TIMESTAMP"
LIST_SESSIONS = "SELECT * FROM user_sessions ORDER BY created_at DESC LIMIT $1 OFFSET $2"
LIST_ACTIVE_SESSIONS = "SELECT * FROM user_sessions WHERE expires_at > CURRENT_TIMESTAMP ORDER BY created_at DESC LIMIT $1 OFFSET $2"
LIST_EXPIRED_SESSIONS = "SELECT * FROM user_sessions WHERE expires_at <= CURRENT_TIMESTAMP"
COUNT_SESSIONS = "SELECT COUNT(*) AS count FROM user_sessions"
COUNT_ACTIVE_SESSIONS = "SELECT COUNT(*) AS count FROM user_sessions WHERE expires_at > CURRENT_TIMESTAMP"
COUNT_EXPIRED_SESSIONS = "SELECT COUNT(*) AS count FROM user_sessions WHERE expires_at <= CURRENT_TIMESTAMP"

# SQL Queries for Permission Repository
GET_PERMISSION_BY_ID = "SELECT * FROM permissions WHERE perm_id = $1"
GET_ROLE_BY_ID = "SELECT * FROM roles WHERE role_id = $1"
GET_ROLE_BY_NAME = "SELECT * FROM roles WHERE role_name = $1"
GET_PERMISSION_BY_CODE = "SELECT * FROM permissions WHERE perm_code = $1"
GET_PERMISSIONS_BY_ROLE = """
        SELECT p.perm_code
        FROM role_perms rp
        JOIN perms p ON rp.perm_id = p.perm_id
        WHERE rp.role_id = $1
        """
GET_PERMISSIONS_FOR_USER = """
        SELECT p.perm_code
        FROM users u
        JOIN roles r ON u.user_role = r.role_id
        JOIN role_perms rp ON r.role_id = rp.role_id
        JOIN perms p ON rp.perm_id = p.perm_id
        WHERE u.user_id = $1;
        """
CREATE_PERMISSION = """
        INSERT INTO perms (perm_code, descr)
        VALUES ($1, $2)
        RETURNING *;
        """
CREATE_ROLE = """
        INSERT INTO roles (role_name, descr)
        VALUES ($1, $2)
        RETURNING *;
        """
CREATE_ROLE_PERMISSION = """
        INSERT INTO role_perms (role_id, perm_id)
        VALUES ($1, $2)
        RETURNING *;
        """
DELETE_ROLE_PERMISSION = "DELETE FROM role_perms WHERE role_id = $1 AND perm_id = $2"
DELETE_ROLE_BY_ID = "DELETE FROM roles WHERE role_id = $1"
DELETE_PERMISSION_BY_ID = "DELETE FROM perms WHERE perm_id = $1"
LIST_ROLES = "SELECT * FROM roles ORDER BY role_name"
LIST_PERMISSIONS = "SELECT * FROM perms ORDER BY perm_code"