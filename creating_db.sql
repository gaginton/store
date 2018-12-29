CREATE database store;
USE store;


CREATE TABLE category (
cat_id INT,
cat_name VARCHAR(30));

CREATE TABLE products (
category VARCHAR(30),
description VARCHAR(30),
price FLOAT,
title VARCHAR(30),
favorite BOOLEAN,
img_url VARCHAR(200),
id INT);

INSERT INTO category
VALUES (16, "cars");

INSERT INTO products
VALUES (16, "This is great!", "1000.0", "Honda2", 0, "https://images.honda.ca/nav.png", 1);  