CREATE TABLE IF NOT EXISTS categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS brands (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    sku          TEXT    NOT NULL UNIQUE,
    title        TEXT    NOT NULL,
    brand_id     INTEGER NOT NULL REFERENCES brands(id),
    category_id  INTEGER NOT NULL REFERENCES categories(id),
    price        REAL    NOT NULL CHECK (price > 0),
    discount_pct REAL,
    stock        INTEGER NOT NULL CHECK (stock >= 0),
    rating       REAL    CHECK (rating BETWEEN 0 AND 5),
    weight       REAL
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_brand    ON products(brand_id);
