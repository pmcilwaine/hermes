CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email char(255) UNIQUE,
    password char(128),
    first_name char(255),
    last_name char(255),
    created TIMESTAMP without time zone,
    modified TIMESTAMP without time zone,
    archived char(1),
    permissions text
);

CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    uuid char(60) UNIQUE,
    url char(255),
    created TIMESTAMP without time zone,
    published char(1),
    type char(100),
    name char(255),
    archived char(1),
    menutitle char(255),
    show_in_menu char(1),
    parent INTEGER,
    path text,
    "user" INTEGER
);

CREATE TABLE job (
    uuid char(60) PRIMARY KEY,
    name char(255),
    status char(10),
    message text
);

INSERT INTO users (email, password, first_name, last_name, created, modified) VALUES ('test@example.org', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Test', 'User', NOW(), NOW());
