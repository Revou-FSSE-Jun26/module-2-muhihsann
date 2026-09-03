    -- Sample data for RevoShop
-- seed.sql


INSERT INTO users (username, email, password_hash, created_at) VALUES
('jean_grey',       'jean.grey@email.com',      'hash_jean_1',  NOW()),
('james_howlett',   'james.howlett@email.com',   'hash_james_2', NOW()),
('kurt_wagner',     'kurt.wagner@email.com',    'hash_kurt_3',  NOW()),
('raven_wagner',    'raven.wagner@email.com',   'hash_raven_4', NOW());

INSERT INTO categories (name, description) VALUES
('Electronics', 'Phones, laptops, and accessories'),
('Home & Kitchen', 'Appliances and kitchenware'),
('Books', 'Fiction and non-fiction titles'),
('Sportswear', 'Athletic clothing and gear');

INSERT INTO products (name, description, price, stock_quantity, category_id, created_at) VALUES
('Wireless Mouse',        'Ergonomic 2.4GHz wireless mouse',      20,  150, 1, NOW()),
('Mechanical Keyboard',   'RGB backlit mechanical keyboard',      90,   60, 1, NOW()),
('Stainless Steel Pan',   '12-inch non-stick frying pan',         35,   80, 2, NOW()),
('Espresso Machine',      'Compact home espresso maker',         199,   25, 2, NOW()),
('The Silent Patient',    'Psychological thriller book',          25,  100, 3, NOW()),
('Atomic Habits',         'Bestselling self-help book',           17,  200, 3, NOW()),
('Running Shoes',         'Lightweight breathable running shoes', 75,  120, 4, NOW()),
('Yoga Mat',              'Non-slip 6mm yoga mat',                25,  140, 4, NOW());

INSERT INTO orders (user_id, order_date, status, total_amount) VALUES
(1, NOW(), 'delivered',  110),
(2, NOW(), 'shipped',     25),
(3, NOW(), 'pending',    234),
(1, NOW(), 'processing',  75),
(4, NOW(), 'delivered',   42);

-- order_items references product prices AT TIME OF PURCHASE
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 20),
(1, 2, 1, 90),
(2, 5, 1, 25),
(3, 4, 1, 199),
(3, 3, 1, 35),
(4, 7, 1, 75),
(5, 6, 1, 17),
(5, 8, 1, 25);