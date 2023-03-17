DROP DATABASE IF EXISTS recipes_db;

CREATE DATABASE recipes_db;

\connect recipes_db

CREATE TABLE users (
    username VARCHAR(25) PRIMARY KEY, 
    password TEXT NOT NULL, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL, 
    email TEXT NOT NULL CHECK (position('@' IN email) > 1)
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL 
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    recipe_name TEXT NOT NULL,
    ingredient TEXT NOT NULL,
    instruction TEXT NOT NULL,
    image_url TEXT NOT NULL,
    user_username VARCHAR REFERENCES users(username) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id)
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, first_name, last_name, email) 
VALUES 
('ollie123', 'test123', 'ollie', 'nzali','ollie@test.com');

INSERT INTO categories (name)
VALUES ('Italian');

INSERT INTO recipes (recipe_name, ingredient, instruction, category_id, image_url, user_username)
VALUES ('Pesto Pasta', 'Pasta, Pesto Sauce, Parmesan Cheese', '1. Cook pasta according to package instructions. 2. Heat pesto sauce in a pan. 3. Drain pasta and add it to the pan with pesto sauce. 4. Add Parmesan cheese and stir well.', 1, 'https://example.com/images/pesto_pasta.jpg', 'ollie123');

INSERT INTO ingredients (name, description, recipe_id)
VALUES ('Pasta', 'Dried pasta', 1), ('Pesto Sauce', 'Prepared pesto sauce', 1), ('Parmesan Cheese', 'Grated Parmesan cheese', 1);