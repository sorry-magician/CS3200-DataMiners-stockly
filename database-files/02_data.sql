USE stockly_db;

-- USERS
-- Must be inserted first — referenced by FK in multiple tables

INSERT INTO Users (full_name, email, role, is_active) VALUES
('Maya Chen',    'maya@stockly.com',    'manager', TRUE),
('Jordan Patel', 'jordan@stockly.com',  'editor',  TRUE),
('Priya Nair',   'priya@stockly.com',   'viewer',  TRUE),
('Alex Torres',  'alex@stockly.com',    'admin',   TRUE);

-- CATEGORIES (10 rows)
-- Inserted in order; category_id auto-assigns 1 through 10

INSERT INTO Categories (category_name) VALUES
('Tops'),        -- category_id = 1
('Bottoms'),     -- category_id = 2
('Dresses'),     -- category_id = 3
('Outerwear'),   -- category_id = 4
('Activewear'),  -- category_id = 5
('Accessories'), -- category_id = 6
('Bags'),        -- category_id = 7
('Footwear'),    -- category_id = 8
('Swimwear'),    -- category_id = 9
('Loungewear');  -- category_id = 10

-- PRODUCTS (40 rows)
-- APR-001 through APR-040
-- Covers: healthy stock, low stock, out of stock,
--         archived, and overstocked scenarios


-- TOPS (category_id = 1)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-001', 'Organic Cotton Crew Tee',
 'Lightweight unisex crew-neck tee made from GOTS-certified organic cotton.',
 29.99, 85, 15, FALSE, 1),

('APR-002', 'Linen Button-Down Shirt',
 'Relaxed-fit button-down woven from European flax linen.',
 54.99, 32, 15, FALSE, 1),

('APR-003', 'Hemp Knit Tank Top',
 'Breathable hemp-blend tank, ideal for warm weather layering.',
 24.99, 6, 12, FALSE, 1),   -- LOW STOCK (6 < 12)

('APR-004', 'Recycled Polyester Hoodie',
 'Midweight pullover hoodie crafted from 100% recycled plastic bottles.',
 74.99, 28, 15, FALSE, 1);


-- BOTTOMS (category_id = 2)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-005', 'Organic Denim Jeans',
 'Classic straight-leg jeans dyed with plant-based indigo.',
 89.99, 41, 12, FALSE, 2),

('APR-006', 'Linen Wide-Leg Trousers',
 'Elegant wide-leg cut in breathable stonewashed linen.',
 69.99, 0, 10, FALSE, 2),   -- OUT OF STOCK (0 < 10)

('APR-007', 'Hemp Cargo Shorts',
 'Durable hemp-canvas cargo shorts with six pockets.',
 49.99, 22, 10, TRUE, 2),   -- ARCHIVED

('APR-008', 'Tencel Wrap Skirt',
 'Fluid wrap skirt in TENCEL Lyocell with adjustable tie waist.',
 59.99, 75, 12, FALSE, 2);  -- OVERSTOCKED (75 >> 12)


-- DRESSES (category_id = 3)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-009', 'Organic Cotton Midi Dress',
 'A-line midi dress in soft organic cotton jersey.',
 94.99, 7, 10, FALSE, 3),   -- LOW STOCK (7 < 10)

('APR-010', 'Linen Sundress',
 'Strappy sundress in lightweight natural linen, fully lined.',
 79.99, 19, 10, FALSE, 3),

('APR-011', 'Recycled Fabric Wrap Dress',
 'Wrap-style dress constructed from deadstock and recycled textiles.',
 84.99, 14, 10, FALSE, 3),

('APR-012', 'Hemp Maxi Dress',
 'Floor-length maxi dress in a hemp-organic cotton blend.',
 99.99, 0, 10, FALSE, 3);   -- OUT OF STOCK (0 < 10)


-- OUTERWEAR (category_id = 4)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-013', 'Organic Wool Overcoat',
 'Structured overcoat in certified organic merino wool blend.',
 189.99, 15, 8, FALSE, 4),

('APR-014', 'Recycled Down Puffer Jacket',
 'Insulated puffer filled with responsibly sourced recycled down.',
 159.99, 22, 8, TRUE, 4),   -- ARCHIVED

('APR-015', 'Hemp Canvas Field Jacket',
 'Four-pocket field jacket in waxed hemp canvas.',
 129.99, 5, 8, FALSE, 4),   -- LOW STOCK (5 < 8)

('APR-016', 'Bamboo Trench Coat',
 'Classic double-breasted trench in bamboo-viscose twill.',
 149.99, 11, 8, FALSE, 4);


-- ACTIVEWEAR (category_id = 5)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-017', 'Recycled Nylon Sports Bra',
 'Medium-support sports bra in chlorine-resistant recycled nylon.',
 39.99, 44, 20, FALSE, 5),

('APR-018', 'Organic Cotton Yoga Pants',
 'High-waist yoga pants in four-way stretch organic cotton.',
 64.99, 67, 20, FALSE, 5),  -- OVERSTOCKED (67 > 20)

('APR-019', 'Hemp Athletic Shorts',
 'Lightweight running shorts in moisture-wicking hemp-blend fabric.',
 34.99, 8, 15, FALSE, 5),   -- LOW STOCK (8 < 15)

('APR-020', 'Tencel Workout Tank',
 'Racerback training tank in cooling TENCEL microfibre.',
 29.99, 31, 15, FALSE, 5);


-- ACCESSORIES (category_id = 6)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-021', 'Organic Cotton Beanie',
 'Ribbed knit beanie in 100% organic combed cotton.',
 19.99, 4, 10, FALSE, 6),   -- LOW STOCK (4 < 10)

('APR-022', 'Recycled Polyester Scarf',
 'Oversized woven scarf made from post-consumer recycled fibres.',
 24.99, 33, 10, FALSE, 6),

('APR-023', 'Hemp Woven Belt',
 'Adjustable woven belt in natural undyed hemp webbing.',
 29.99, 62, 12, FALSE, 6),  -- OVERSTOCKED (62 >> 12)

('APR-024', 'Bamboo Sunglasses Case',
 'Slim hard case for sunglasses, made from pressed bamboo.',
 14.99, 18, 10, TRUE, 6);   -- ARCHIVED


-- BAGS (category_id = 7)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-025', 'Organic Canvas Tote Bag',
 'Large market tote in 12oz organic cotton canvas with inside pocket.',
 34.99, 48, 15, FALSE, 7),

('APR-026', 'Hemp Crossbody Bag',
 'Compact zip-top crossbody bag in natural hemp canvas.',
 49.99, 21, 12, FALSE, 7),

('APR-027', 'Recycled Material Backpack',
 '20L daypack constructed from recycled ocean-bound plastics.',
 79.99, 9, 12, FALSE, 7),   -- LOW STOCK (9 < 12)

('APR-028', 'Linen Clutch Purse',
 'Evening clutch in stonewashed linen with brass zip closure.',
 39.99, 17, 10, TRUE, 7);   -- ARCHIVED


-- FOOTWEAR (category_id = 8)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-029', 'Cork-Sole Sandals',
 'Open-toe sandals with a contoured cork footbed and hemp upper.',
 59.99, 24, 10, FALSE, 8),

('APR-030', 'Organic Canvas Sneakers',
 'Low-top lace-up sneakers in organic cotton canvas with natural rubber sole.',
 74.99, 35, 12, FALSE, 8),

('APR-031', 'Hemp Slip-On Shoes',
 'Casual slip-ons in woven hemp with a recycled rubber outsole.',
 54.99, 80, 12, FALSE, 8),  -- OVERSTOCKED (80 >> 12)

('APR-032', 'Recycled Rubber Rain Boots',
 'Knee-high rain boots vulcanised from reclaimed natural rubber.',
 119.99, 13, 8, FALSE, 8);


-- SWIMWEAR (category_id = 9)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-033', 'Recycled Nylon One-Piece Swimsuit',
 'Chlorine-resistant one-piece made from 78% recycled nylon.',
 69.99, 6, 10, FALSE, 9),   -- LOW STOCK (6 < 10)

('APR-034', 'Organic Cotton Swim Trunks',
 'Quick-dry swim trunks in organic cotton and recycled polyester blend.',
 44.99, 15, 10, FALSE, 9),

('APR-035', 'Hemp Bikini Set',
 'Two-piece bikini in soft hemp-organic cotton blend.',
 59.99, 11, 8, TRUE, 9),    -- ARCHIVED

('APR-036', 'Tencel Beach Cover-Up',
 'Lightweight kaftan-style cover-up in TENCEL Modal.',
 54.99, 19, 8, FALSE, 9);


-- LOUNGEWEAR (category_id = 10)
INSERT INTO Products
  (sku, product_name, description, unit_price,
   quantity_on_hand, reorder_threshold, is_archived, category_id)
VALUES
('APR-037', 'Organic Cotton Pajama Set',
 'Long-sleeve top and straight-leg pant set in organic cotton flannel.',
 79.99, 27, 12, FALSE, 10),

('APR-038', 'Bamboo Terry Robe',
 'Plush full-length robe in ultra-soft bamboo terry cloth.',
 94.99, 7, 10, FALSE, 10),  -- LOW STOCK (7 < 10)

('APR-039', 'Hemp Lounge Pants',
 'Drawstring lounge pants in a hemp-organic cotton jersey blend.',
 44.99, 33, 12, FALSE, 10),

('APR-040', 'Recycled Fleece Pullover',
 'Cosy midlayer pullover in anti-pill recycled polyester fleece.',
 64.99, 3, 15, FALSE, 10);  -- LOW STOCK (3 < 15)

 -- SYSTEM CONFIG
INSERT INTO System_Config (config_key, config_value, user_id) VALUES
('low_stock_default', '10', 4),
('currency', 'USD', 4),
('timezone', 'America/New_York', 4),
('company_name', 'Stockly Demo Store', 4),
('reorder_alert_email', 'alerts@stockly.com', 4);

-- AUDIT LOG
INSERT INTO Audit_Log (action_type, table_name, record_ref, is_flagged, user_id) VALUES
('INSERT', 'Products', 'APR-001', FALSE, 1),
('UPDATE', 'Products', 'APR-001', FALSE, 1),
('INSERT', 'Products', 'APR-047', FALSE, 2),
('UPDATE', 'Stock_Adjustments', 'APR-022', TRUE, 2),
('INSERT', 'Purchase_Orders', 'PO-001', FALSE, 2),
('UPDATE', 'Purchase_Orders', 'PO-001', FALSE, 2),
('INSERT', 'Users', 'jordan@stockly.com', FALSE, 4),
('DELETE', 'Products', 'APR-007', TRUE, 4),
('UPDATE', 'System_Config', 'low_stock_default', FALSE, 4),
('INSERT', 'Sales_Orders', 'SO-001', FALSE, 1);

