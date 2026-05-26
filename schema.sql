-- schema.sql: Example table creation
CREATE TABLE IF NOT EXISTS new (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into the new table
INSERT INTO new (username, email) VALUES ('testuser', 'testuser@example.com'),
                                         ('anotheruser', 'another@example.com');

-- Create an index on the username column for faster lookups
CREATE INDEX IF NOT EXISTS idx_new_username ON new (username);


-- Create satya_users table
CREATE TABLE IF NOT EXISTS satya_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL
);

-- Insert users (use 'name' instead of 'username')
INSERT INTO satya_users (name, email) VALUES ('testuser', 'test@example.com');
INSERT INTO satya_users (name, email) VALUES ('thirduser', 'saone@example.com');

-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    owner_id INTEGER NOT NULL,
    files VARCHAR,
    images VARCHAR
);

-- Insert items (use 'items' not 'iteams', and correct columns)
INSERT INTO items (title, description, owner_id) VALUES ('Item 1', 'Description 1', 1);
INSERT INTO items (title, description, owner_id) VALUES ('Item 2', 'Description 2', 1);


