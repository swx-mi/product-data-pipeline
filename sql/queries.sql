-- Run with:  sqlite3 products.db < sql/queries.sql

-- 1. Number of products per category (largest first)
SELECT c.name AS category, COUNT(*) AS product_count
FROM products p
JOIN categories c ON c.id = p.category_id
GROUP BY c.name
ORDER BY product_count DESC;

-- 2. Average price and total stock per brand (top 10 by stock)
SELECT b.name AS brand,
       ROUND(AVG(p.price), 2) AS avg_price,
       SUM(p.stock)           AS total_stock
FROM products p
JOIN brands b ON b.id = p.brand_id
GROUP BY b.name
ORDER BY total_stock DESC
LIMIT 10;

-- 3. Duplicate title detection (same title under different SKUs)
SELECT LOWER(title) AS title, COUNT(*) AS occurrences
FROM products
GROUP BY LOWER(title)
HAVING COUNT(*) > 1;

-- 4. Low-stock products (fewer than 10 units)
SELECT sku, title, stock
FROM products
WHERE stock < 10
ORDER BY stock ASC;

-- 5. Products with no real brand (data-quality check)
SELECT p.sku, p.title
FROM products p
JOIN brands b ON b.id = p.brand_id
WHERE b.name = 'Unbranded';

-- 6. Most expensive product in each category (subquery)
SELECT c.name AS category, p.title, p.price
FROM products p
JOIN categories c ON c.id = p.category_id
WHERE p.price = (
    SELECT MAX(p2.price) FROM products p2 WHERE p2.category_id = p.category_id
)
ORDER BY p.price DESC;

-- 7. Categories whose average rating is below the overall average
SELECT c.name AS category, ROUND(AVG(p.rating), 2) AS avg_rating
FROM products p
JOIN categories c ON c.id = p.category_id
GROUP BY c.name
HAVING AVG(p.rating) < (SELECT AVG(rating) FROM products)
ORDER BY avg_rating;
