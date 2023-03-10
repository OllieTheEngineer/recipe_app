CREATE DATABASE recipes_db;

DROP DATABASE recipes_db;
\connect recipes_db

CREATE TABLE users ( 
    username VARCHAR(25) PRIMARY KEY, 
    password TEXT NOT NULL, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL, 
    email TEXT NOT NULL CHECK (position('@' IN email) > 1)
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    recipe_name TEXT NOT NULL,
    ingredient TEXT NOT NULL,
    instruction TEXT NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT NOT NULL
    REFERENCES users ON DELETE CASCADE
);



CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    recipes_id INTEGER REFERENCES recipes ON DELETE CASCADE
);