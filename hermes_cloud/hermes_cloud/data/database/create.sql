CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email char(255) UNIQUE,
    password char(128),
    first_name char(255),
    last_name char(255),
    created TIMESTAMP without time zone,
    modified TIMESTAMP without time zone,
    archived BOOL,
    permissions text
);

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    uuid char(36) UNIQUE,
    url char(255),
    created TIMESTAMP without time zone,
    published BOOL,
    type char(100),
    name char(255),
    archived BOOL,
    menutitle char(255),
    show_in_menu BOOL,
    parent INTEGER,
    path text,
    user_id INTEGER
);

CREATE TABLE job (
    id SERIAL PRIMARY KEY,
    uuid char(36) UNIQUE,
    name char(255),
    status char(10),
    created TIMESTAMP without time zone,
    modified TIMESTAMP without time zone,
    message text
);

INSERT INTO users (email, password, first_name, last_name, created, modified, permissions) VALUES ('test@example.org', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Test', 'User', NOW(), NOW(), '');
