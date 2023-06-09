DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS invoice;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code INTEGER UNIQUE,
  name TEXT NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE invoice (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_code INTEGER NOT NULL,
  quantity REAL NOT NULL,
  FOREIGN KEY (product_code) REFERENCES product (code)
);