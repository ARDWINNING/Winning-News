CREATE EXTENSION IF NOT EXISTS "pgcrypto";
Create EXTENSION IF NOT EXISTS "citext";

-- Enums
CREATE TYPE user_role AS ENUM ('reader', 'writer', 'editor', 'admin');
CREATE TYPE user_status AS ENUM ('active', 'pending_verification', 'banned');
CREATE TYPE article_category AS ENUM ('Politics', 'Technology', 'Health', 'Sports', 'Entertainment', 'Business', 'Science', 'World');

-- Users table
CREATE TABLE IF NOT EXISTS users (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- User Info
  email CITEXT UNIQUE NOT NULL CHECK (char_length(email) <= 254), -- RFC 3696 compliant
  username CITEXT UNIQUE NOT NULL CHECK (char_length(username) <= 15), -- 1.1Mn^15 possible usernames
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  -- Password is never stored in plaintext set max input length to 20 chars
  password_hash bytea NOT NULL, -- 32 bytes argon2id manual output
  password_salt bytea NOT NULL, -- 32 bytes salt 2^256 possible salts
  -- Roles & Types
  user_type user_role NOT NULL DEFAULT 'reader', -- user roles enumerated above
  status_type user_status NOT NULL DEFAULT 'pending_verification',
  -- Timestamps
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- updated via trigger on row update
  last_login TIMESTAMPTZ
);

-- News_Organisations table
CREATE TABLE IF NOT EXISTS news_organisations (
  org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_name CITEXT UNIQUE NOT NULL, -- to appear underneath writer name
  website_url TEXT -- to make it clickable on articles
);

-- Writer profiles table
CREATE TABLE IF NOT EXISTS writer_profiles (
  user_id UUID PRIMARY KEY REFERENCES users(id),
  org_id UUID REFERENCES news_organisations(org_id) NOT NULL ON DELETE RESTRICT, -- 15 char max length
  bio TEXT, -- brief biography of the writer
  profile_image_url TEXT -- referential URL pointing to image hosting solution
);

-- Articles table
CREATE TABLE IF NOT EXISTS articles (
  -- IDs
  article_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  writer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  -- Article header
  title VARCHAR(80) NOT NULL, -- Capped at 80 chars for better readability
  slug CITEXT UNIQUE NOT NULL CHECK (char_length(slug) <= 20), -- unique URL friendly title max 20 char
  category article_category NOT NULL, -- enumerated categories
  tags TEXT[], -- array of tags for better searchability
  featured_image_url TEXT, -- referential URL pointing to image hosting solution
  -- Article body
  excerpt TEXT, -- may delete later if not needed
  content TEXT NOT NULL,  -- main article content, formatt to be decided later
  -- Publication info
  is_published BOOLEAN DEFAULT FALSE, -- whether article is published or draft
  published_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  -- session token is not saved only sent to user in cookie
  token_hash bytea UNIQUE NOT NULL, -- 32 bytes derived from a sha-256 hash of session token
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP + INTERVAL '24 hours' -- set as needed
);

-- Trigger functions
CREATE OR REPLACE FUNCTION user_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_user_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION user_updated_at();

CREATE OR REPLACE FUNCTION articles_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_articles_updated_at
BEFORE UPDATE ON articles
FOR EACH ROW
EXECUTE FUNCTION articles_updated_at();

-- Indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_writers_org ON writer_profiles(org_id);
CREATE INDEX idx_articles_writer ON articles(writer_id);
CREATE INDEX idx_articles_title ON articles(title);
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_category ON articles(category);
CREATE INDEX idx_articles_tags ON articles USING GIN(tags);
CREATE INDEX idx_articles_time ON articles(published_at);
CREATE INDEX idx_sessions_expiry ON user_sessions(expires_at);