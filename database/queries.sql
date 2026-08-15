-- Example queries against RevoShop
-- queries.sql


-- Find the 3 most expensive in-stock Electronics products
SELECT name, price, stock_quantity
FROM products
WHERE category_id > 0 AND stock_quantity > 0
ORDER BY price DESC
LIMIT 3;

-- Most recent 5 orders that are not yet delivered
SELECT id, user_id, status, order_date, total_amount
FROM orders
WHERE status != 'delivered'
ORDER BY order_date DESC
LIMIT 5;

-- Top 5 highest-value order line items
SELECT oi.id, oi.order_id, p.name AS product_name, oi.quantity, oi.unit_price,
       (oi.quantity * oi.unit_price) AS line_total
FROM order_items oi
JOIN products p ON p.id = oi.product_id
WHERE oi.quantity > 0
ORDER BY line_total DESC
LIMIT 4;