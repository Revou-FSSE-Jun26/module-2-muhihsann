-- Sample data for RevoShop
-- seed.sql


INSERT INTO users (username, email, password_hash) VALUES
('jean_grey',    	   'jean.grey@email.com',    'hash_jean_1'),
('james_howlett',  'james.howlett@email.com',   'hash_james_2'),
('kurt_wagner',		 'kurt.wagner@email.com',	 'hash_kurt_3'),
('raven_wagner',    'raven.wagner@email.com', 	'hash_raven_4');

INSERT INTO categories (name, description) VALUES
('Electronics', 'Phones, laptops, and accessories'),
('Home & Kitchen', 'Appliances and kitchenware'),
('Books', 'Fiction and non-fiction titles'),
('Sportswear', 'Athletic clothing and gear');

INSERT INTO products (name, description, price, stock_quantity, category_id) VALUES
('Wireless Mouse',        'Ergonomic 2.4GHz wireless mouse',      20,  150, 1),
('Mechanical Keyboard',   'RGB backlit mechanical keyboard',      90,   60, 1),
('Stainless Steel Pan',   '12-inch non-stick frying pan',         35,   80, 2),
('Espresso Machine',      'Compact home espresso maker',         199,   25, 2),
('The Silent Patient',	  'Psychological thriller book',  		  25,  100, 3),
('Atomic Habits',         'Bestselling self-help book',           17,  200, 3),
('Running Shoes',         'Lightweight breathable running shoes', 75,  120, 4),
('Yoga Mat',              'Non-slip 6mm yoga mat',                25,  140, 4);

INSERT INTO orders (user_id, status, total_amount) VALUES
(1, 'delivered',  110),
(2, 'shipped',     25),
(3, 'pending',    234),
(1, 'processing',  75),
(4, 'delivered',   42);

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