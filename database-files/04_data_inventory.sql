USE stockly_db;

INSERT INTO Suppliers (supplier_name, contact_email, contact_phone, is_active, lead_time_days) VALUES
('GreenWeave Co.',         'orders@greenweave.com',       '617-555-0101', TRUE,   7),
('EcoFabrics Inc.',        'supply@ecofabrics.com',       '617-555-0102', TRUE,  14),
('ThreadCraft Supply',     'info@threadcraft.com',        '617-555-0103', TRUE,   9),
('Urban Textile Group',    'sales@urbantextile.com',      '617-555-0104', TRUE,  21),
('Pacific Stitch Co.',     'contact@pacificstitch.com',   '617-555-0105', TRUE,  12),
('SilkRoute Traders',      'trade@silkroute.com',         '617-555-0106', TRUE,  30),
('Coastal Canvas Ltd.',    'orders@coastalcanvas.com',    '617-555-0107', TRUE,  18),
('Nordic Fiber Works',     'fiber@nordicworks.com',       '617-555-0108', TRUE,  25),
('Summit Apparel Supply',  'supply@summitapparel.com',    '617-555-0109', TRUE,   9),
('TerraThread Co.',        'hello@terrathread.com',       '617-555-0110', TRUE,  15),
('BlueLine Fabrics',       'sales@bluelinefabrics.com',   '617-555-0111', TRUE,  11),
('Meridian Textile Co.',   'orders@meridiantextile.com',  '617-555-0112', TRUE,  20),
('Alpine Stitch Ltd.',     'info@alpinestitch.com',       '617-555-0113', TRUE,  13),
('Harbor Cloth Works',     'supply@harborcloth.com',      '617-555-0114', TRUE,  17),
('Sunrise Fabric Group',   'contact@sunrisefabric.com',   '617-555-0115', TRUE,   8),
('Canyon Apparel Supply',  'sales@canyonapparel.com',     '617-555-0116', TRUE,  22),
('Cascade Textile Co.',    'orders@cascadetextile.com',   '617-555-0117', TRUE,  16),
('Delta Fabric Works',     'info@deltafabric.com',        '617-555-0118', TRUE,  14),
('Empire Thread Co.',      'sales@empirethread.com',      '617-555-0119', TRUE,  19),
('Forest Weave Ltd.',      'supply@forestweave.com',      '617-555-0120', TRUE,  28),
('Golden Gate Fabrics',    'orders@goldengatefab.com',    '617-555-0121', TRUE,  10),
('Highland Cloth Co.',     'info@highlandcloth.com',      '617-555-0122', TRUE,  24),
('Ironwood Textile Group', 'sales@ironwoodtextile.com',   '617-555-0123', TRUE,  33),
('Jade River Fabrics',     'orders@jaderiverfab.com',     '617-555-0124', TRUE,  12),
('Keystone Apparel Ltd.',  'supply@keystoneapparel.com',  '617-555-0125', TRUE,  15),
('Lakeside Thread Co.',    'info@lakesidethread.com',     '617-555-0126', TRUE,  20),
('Mountain Weave Works',   'sales@mountainweave.com',     '617-555-0127', TRUE,   7),
('NorthStar Fabrics',      'orders@northstarfab.com',     '617-555-0128', TRUE,  18),
('Oakridge Textile Co.',   'info@oakridgetextile.com',    '617-555-0129', TRUE,  11),
('Prairie Stitch Supply',  'supply@prairiestitch.com',    '617-555-0130', TRUE,  26),
('Riverdale Cloth Ltd.',   'orders@riverdalecloth.com',   '617-555-0131', TRUE,  14),
('Stonegate Fabrics',      'info@stonegatefab.com',       '617-555-0132', TRUE,   9),
('Timber Trail Textiles',  'sales@timbertrail.com',       '617-555-0133', TRUE,  22),
('Unity Weave Group',      'orders@unityweave.com',       '617-555-0134', TRUE,  16),
('Valley Fabric Co.',      'supply@valleyfabric.com',     '617-555-0135', FALSE, 30);
-- Note: supplier_id 35 (Valley Fabric Co.) is inactive — used to demonstrate
--       the deactivate-supplier feature in the UI.


-- =============================================================
-- PRODUCT_SUPPLIERS  (130 rows)
-- Each SKU gets 3 suppliers; APR-031..040 get 4.
-- Total: 30×3 + 10×4 = 130 rows
--
-- Supplier groups:
--   APR-001..010 → suppliers  1,  5,  9
--   APR-011..020 → suppliers  2,  8, 15
--   APR-021..030 → suppliers  3, 12, 20
--   APR-031..040 → suppliers  4, 11, 18, 27
-- =============================================================
INSERT INTO Product_Suppliers (sku, supplier_id) VALUES
-- APR-001 to APR-010
('APR-001', 1), ('APR-001', 5), ('APR-001', 9),
('APR-002', 1), ('APR-002', 5), ('APR-002', 9),
('APR-003', 1), ('APR-003', 5), ('APR-003', 9),
('APR-004', 1), ('APR-004', 5), ('APR-004', 9),
('APR-005', 1), ('APR-005', 5), ('APR-005', 9),
('APR-006', 1), ('APR-006', 5), ('APR-006', 9),
('APR-007', 1), ('APR-007', 5), ('APR-007', 9),
('APR-008', 1), ('APR-008', 5), ('APR-008', 9),
('APR-009', 1), ('APR-009', 5), ('APR-009', 9),
('APR-010', 1), ('APR-010', 5), ('APR-010', 9),
-- APR-011 to APR-020
('APR-011', 2), ('APR-011', 8), ('APR-011', 15),
('APR-012', 2), ('APR-012', 8), ('APR-012', 15),
('APR-013', 2), ('APR-013', 8), ('APR-013', 15),
('APR-014', 2), ('APR-014', 8), ('APR-014', 15),
('APR-015', 2), ('APR-015', 8), ('APR-015', 15),
('APR-016', 2), ('APR-016', 8), ('APR-016', 15),
('APR-017', 2), ('APR-017', 8), ('APR-017', 15),
('APR-018', 2), ('APR-018', 8), ('APR-018', 15),
('APR-019', 2), ('APR-019', 8), ('APR-019', 15),
('APR-020', 2), ('APR-020', 8), ('APR-020', 15),
-- APR-021 to APR-030
('APR-021', 3), ('APR-021', 12), ('APR-021', 20),
('APR-022', 3), ('APR-022', 12), ('APR-022', 20),
('APR-023', 3), ('APR-023', 12), ('APR-023', 20),
('APR-024', 3), ('APR-024', 12), ('APR-024', 20),
('APR-025', 3), ('APR-025', 12), ('APR-025', 20),
('APR-026', 3), ('APR-026', 12), ('APR-026', 20),
('APR-027', 3), ('APR-027', 12), ('APR-027', 20),
('APR-028', 3), ('APR-028', 12), ('APR-028', 20),
('APR-029', 3), ('APR-029', 12), ('APR-029', 20),
('APR-030', 3), ('APR-030', 12), ('APR-030', 20),
-- APR-031 to APR-040  (4 suppliers each)
('APR-031', 4), ('APR-031', 11), ('APR-031', 18), ('APR-031', 27),
('APR-032', 4), ('APR-032', 11), ('APR-032', 18), ('APR-032', 27),
('APR-033', 4), ('APR-033', 11), ('APR-033', 18), ('APR-033', 27),
('APR-034', 4), ('APR-034', 11), ('APR-034', 18), ('APR-034', 27),
('APR-035', 4), ('APR-035', 11), ('APR-035', 18), ('APR-035', 27),
('APR-036', 4), ('APR-036', 11), ('APR-036', 18), ('APR-036', 27),
('APR-037', 4), ('APR-037', 11), ('APR-037', 18), ('APR-037', 27),
('APR-038', 4), ('APR-038', 11), ('APR-038', 18), ('APR-038', 27),
('APR-039', 4), ('APR-039', 11), ('APR-039', 18), ('APR-039', 27),
('APR-040', 4), ('APR-040', 11), ('APR-040', 18), ('APR-040', 27);


-- =============================================================
-- PURCHASE_ORDERS  (60 rows)
-- POs 1-20:  status = 'received'  (April – September 2024)
-- POs 21-40: status = 'in_transit' (October 2024 – February 2025)
-- POs 41-60: status = 'ordered'   (March – April 2025)
-- All created by user_id = 2 (Jordan Patel, inventory manager)
-- =============================================================
INSERT INTO Purchase_Orders (order_date, expected_delivery_date, status, notes, supplier_id, user_id) VALUES
-- ── RECEIVED ──────────────────────────────────────────────────────────────
('2024-04-05', '2024-04-15', 'received', 'Spring collection tops restock',         1,  2),
('2024-04-12', '2024-04-26', 'received', 'Initial summer bag order',               3,  2),
('2024-04-22', '2024-05-06', 'received', 'Bottoms line mid-season restock',        5,  2),
('2024-05-01', '2024-05-15', 'received', 'Accessories reorder',                    8,  2),
('2024-05-10', '2024-05-24', 'received', 'Pre-season outerwear order',             2,  2),
('2024-05-18', '2024-06-01', 'received', 'Tops mid-season replenishment',         10,  2),
('2024-06-02', '2024-06-16', 'received', 'Summer sale inventory build',           12,  2),
('2024-06-15', '2024-06-29', 'received', 'Bags collection update',                15,  2),
('2024-06-22', '2024-07-06', 'received', 'Footwear accessories order',            18,  2),
('2024-07-01', '2024-07-15', 'received', 'Mid-year full inventory refresh',       20,  2),
('2024-07-10', '2024-07-24', 'received', 'Back-to-basics collection restock',     22,  2),
('2024-07-20', '2024-08-03', 'received', 'Clearance prep — extra units',          25,  2),
('2024-08-05', '2024-08-19', 'received', 'Fall preview item order',               28,  2),
('2024-08-15', '2024-08-29', 'received', 'Classic tops bulk reorder',             30,  2),
('2024-08-25', '2024-09-08', 'received', 'Premium fabric accessories batch',       1,  2),
('2024-09-03', '2024-09-17', 'received', 'Fall collection launch PO',              3,  2),
('2024-09-12', '2024-09-26', 'received', 'Autumn bottoms line restock',            5,  2),
('2024-09-20', '2024-10-04', 'received', 'Holiday inventory prep',                 8,  2),
('2024-09-28', '2024-10-12', 'received', 'Winter bag collection order',           10,  2),
('2024-10-05', '2024-10-19', 'received', 'Q4 full stock replenishment',           12,  2),
-- ── IN TRANSIT ────────────────────────────────────────────────────────────
('2024-10-15', '2024-10-29', 'in_transit', 'Winter outerwear bulk order',         15,  2),
('2024-10-25', '2024-11-08', 'in_transit', 'Holiday accessories batch',           18,  2),
('2024-11-01', '2024-11-15', 'in_transit', 'Black Friday stock build',            20,  2),
('2024-11-08', '2024-11-22', 'in_transit', 'Premium tops — winter line',          22,  2),
('2024-11-15', '2024-11-29', 'in_transit', 'Gift-season bag orders',              25,  2),
('2024-11-22', '2024-12-06', 'in_transit', 'Year-end inventory build',            28,  2),
('2024-12-01', '2024-12-15', 'in_transit', 'December mid-month restock',          30,  2),
('2024-12-10', '2024-12-24', 'in_transit', 'Holiday bottoms collection',           2,  2),
('2024-12-18', '2025-01-01', 'in_transit', 'New-year inventory prep',              4,  2),
('2024-12-28', '2025-01-11', 'in_transit', 'Post-holiday core reorder',            6,  2),
('2025-01-05', '2025-01-19', 'in_transit', 'Winter clearance support items',       9,  2),
('2025-01-12', '2025-01-26', 'in_transit', 'Spring preview stock',                11,  2),
('2025-01-20', '2025-02-03', 'in_transit', 'New spring tops order',               13,  2),
('2025-01-28', '2025-02-11', 'in_transit', 'Accessories spring launch',           16,  2),
('2025-02-03', '2025-02-17', 'in_transit', 'Q1 inventory refresh',                19,  2),
('2025-02-10', '2025-02-24', 'in_transit', 'Spring bag collection',               21,  2),
('2025-02-17', '2025-03-03', 'in_transit', 'New arrivals — bottoms',              24,  2),
('2025-02-24', '2025-03-10', 'in_transit', 'Mid-season restock',                  27,  2),
('2025-03-01', '2025-03-15', 'in_transit', 'Spring outerwear order',              29,  2),
('2025-03-08', '2025-03-22', 'in_transit', 'Fresh-season accessories',            32,  2),
-- ── ORDERED ───────────────────────────────────────────────────────────────
('2025-03-12', '2025-03-26', 'ordered', 'Spring restock batch A',                 33,  2),
('2025-03-15', '2025-03-29', 'ordered', 'New color-variant tops',                 34,  2),
('2025-03-18', '2025-04-01', 'ordered', 'Q2 bag refresh',                          1,  2),
('2025-03-20', '2025-04-03', 'ordered', 'Bottoms reorder — spring',                3,  2),
('2025-03-22', '2025-04-05', 'ordered', 'Accessories new line',                    5,  2),
('2025-03-24', '2025-04-07', 'ordered', 'Lightweight outerwear order',             7,  2),
('2025-03-26', '2025-04-09', 'ordered', 'Premium tops Q2',                         9,  2),
('2025-03-28', '2025-04-11', 'ordered', 'Summer preview inventory',               11,  2),
('2025-03-30', '2025-04-13', 'ordered', 'Bag collection update',                  13,  2),
('2025-04-01', '2025-04-15', 'ordered', 'Core basics restock',                    15,  2),
('2025-04-03', '2025-04-17', 'ordered', 'New arrivals — accessories',             17,  2),
('2025-04-05', '2025-04-19', 'ordered', 'Spring tops final order',                19,  2),
('2025-04-07', '2025-04-21', 'ordered', 'Summer bottoms Q2',                      21,  2),
('2025-04-08', '2025-04-22', 'ordered', 'Q2 outerwear stock',                     23,  2),
('2025-04-09', '2025-04-23', 'ordered', 'Accessories volume order',               26,  2),
('2025-04-10', '2025-04-24', 'ordered', 'New season bags',                        28,  2),
('2025-04-11', '2025-04-25', 'ordered', 'Tops restock — spring',                  31,  2),
('2025-04-12', '2025-04-26', 'ordered', 'Bottoms summer prep',                    33,  2),
('2025-04-13', '2025-04-27', 'ordered', 'Final Q2 accessories order',             34,  2),
('2025-04-14', '2025-04-28', 'ordered', 'Full spring collection restock',          2,  2);


-- =============================================================
-- PO_PRODUCTS  (160 rows)
-- POs  1-20 (received)   → 3 line items each = 60
-- POs 21-40 (in_transit) → 2 line items each = 40
-- POs 41-60 (ordered)    → 3 line items each = 60
-- Total: 160 rows (satisfies 125+ requirement)
-- =============================================================

-- POs 1-20: 3 items each
INSERT INTO PO_Products (sku, po_id, quantity_ordered) VALUES
('APR-001', 1, 80), ('APR-002', 1, 50), ('APR-003', 1, 40),
('APR-005', 2, 60), ('APR-025', 2, 45), ('APR-026', 2, 30),
('APR-006', 3, 55), ('APR-008', 3, 40), ('APR-010', 3, 35),
('APR-021', 4, 50), ('APR-022', 4, 40), ('APR-023', 4, 60),
('APR-013', 5, 30), ('APR-015', 5, 25), ('APR-016', 5, 20),
('APR-001', 6, 70), ('APR-004', 6, 45), ('APR-020', 6, 35),
('APR-017', 7, 60), ('APR-018', 7, 55), ('APR-019', 7, 40),
('APR-025', 8, 50), ('APR-027', 8, 35), ('APR-026', 8, 40),
('APR-029', 9, 30), ('APR-030', 9, 25), ('APR-031', 9, 20),
('APR-005', 10, 55), ('APR-006', 10, 45), ('APR-008', 10, 35),
('APR-009', 11, 40), ('APR-011', 11, 30), ('APR-012', 11, 25),
('APR-017', 12, 65), ('APR-018', 12, 50), ('APR-020', 12, 40),
('APR-013', 13, 20), ('APR-016', 13, 15), ('APR-040', 13, 30),
('APR-001', 14, 100),('APR-002', 14, 75), ('APR-004', 14, 50),
('APR-021', 15, 45), ('APR-022', 15, 55), ('APR-024', 15, 30),
('APR-013', 16, 25), ('APR-015', 16, 20), ('APR-016', 16, 18),
('APR-005', 17, 60), ('APR-006', 17, 50), ('APR-007', 17, 35),
('APR-025', 18, 55), ('APR-026', 18, 40), ('APR-027', 18, 30),
('APR-025', 19, 60), ('APR-026', 19, 45), ('APR-028', 19, 20),
('APR-003', 20, 50), ('APR-019', 20, 40), ('APR-033', 20, 30);

-- POs 21-40: 2 items each
INSERT INTO PO_Products (sku, po_id, quantity_ordered) VALUES
('APR-013', 21, 35), ('APR-016', 21, 25),
('APR-021', 22, 50), ('APR-022', 22, 40),
('APR-001', 23, 90), ('APR-004', 23, 60),
('APR-001', 24, 70), ('APR-002', 24, 55),
('APR-025', 25, 45), ('APR-026', 25, 35),
('APR-013', 26, 30), ('APR-037', 26, 25),
('APR-037', 27, 40), ('APR-038', 27, 30),
('APR-008', 28, 55), ('APR-006', 28, 45),
('APR-039', 29, 35), ('APR-040', 29, 25),
('APR-037', 30, 40), ('APR-038', 30, 30),
('APR-039', 31, 30), ('APR-040', 31, 20),
('APR-003', 32, 45), ('APR-019', 32, 35),
('APR-001', 33, 80), ('APR-002', 33, 60),
('APR-021', 34, 50), ('APR-023', 34, 40),
('APR-009', 35, 30), ('APR-011', 35, 25),
('APR-025', 36, 55), ('APR-026', 36, 40),
('APR-006', 37, 50), ('APR-008', 37, 40),
('APR-003', 38, 40), ('APR-019', 38, 30),
('APR-013', 39, 25), ('APR-015', 39, 20),
('APR-021', 40, 45), ('APR-022', 40, 35);

-- POs 41-60: 3 items each
INSERT INTO PO_Products (sku, po_id, quantity_ordered) VALUES
('APR-001', 41, 75), ('APR-003', 41, 50), ('APR-004', 41, 40),
('APR-001', 42, 80), ('APR-002', 42, 60), ('APR-020', 42, 35),
('APR-025', 43, 55), ('APR-026', 43, 40), ('APR-027', 43, 30),
('APR-005', 44, 60), ('APR-006', 44, 50), ('APR-008', 44, 35),
('APR-021', 45, 50), ('APR-022', 45, 45), ('APR-023', 45, 40),
('APR-013', 46, 25), ('APR-015', 46, 20), ('APR-016', 46, 15),
('APR-001', 47, 90), ('APR-002', 47, 70), ('APR-004', 47, 50),
('APR-017', 48, 55), ('APR-018', 48, 45), ('APR-019', 48, 40),
('APR-025', 49, 50), ('APR-026', 49, 40), ('APR-028', 49, 20),
('APR-001', 50, 100),('APR-003', 50, 60), ('APR-020', 50, 40),
('APR-021', 51, 50), ('APR-022', 51, 40), ('APR-024', 51, 25),
('APR-001', 52, 80), ('APR-002', 52, 65), ('APR-004', 52, 45),
('APR-005', 53, 55), ('APR-006', 53, 45), ('APR-008', 53, 30),
('APR-013', 54, 30), ('APR-015', 54, 25), ('APR-016', 54, 20),
('APR-021', 55, 55), ('APR-022', 55, 45), ('APR-023', 55, 35),
('APR-025', 56, 60), ('APR-026', 56, 50), ('APR-027', 56, 35),
('APR-001', 57, 85), ('APR-002', 57, 65), ('APR-004', 57, 45),
('APR-005', 58, 60), ('APR-008', 58, 50), ('APR-019', 58, 35),
('APR-021', 59, 50), ('APR-022', 59, 40), ('APR-024', 59, 25),
('APR-001', 60, 120),('APR-003', 60, 80), ('APR-004', 60, 60);


-- =============================================================
-- STOCK_ADJUSTMENTS  (60 rows)
-- 30 'damaged'    (negative quantity_delta)
-- 30 'correction' (mixed positive/negative)
-- References user_ids 1-4; SKUs from APR-001..040
-- =============================================================
INSERT INTO Stock_Adjustments (reason, quantity_delta, adjustment_type, sku, user_id) VALUES
-- ── DAMAGED (30 rows) ─────────────────────────────────────────────────────
('Water damage during warehouse storage',         -2, 'damaged', 'APR-001', 2),
('Shipping transit damage — torn seams',          -3, 'damaged', 'APR-002', 2),
('Mold found during inventory check',             -5, 'damaged', 'APR-003', 2),
('Staining from a warehouse spill',               -4, 'damaged', 'APR-005', 2),
('Pest damage to stored items',                   -2, 'damaged', 'APR-006', 2),
('Customer return — item unsellable',             -1, 'damaged', 'APR-008', 2),
('Torn label during fulfillment',                 -3, 'damaged', 'APR-009', 2),
('Fire sprinkler water damage',                   -7, 'damaged', 'APR-010', 2),
('Fading from direct sun exposure',               -2, 'damaged', 'APR-011', 2),
('Zipper defect found during QC check',           -4, 'damaged', 'APR-013', 2),
('Seam failure on bulk lot',                      -6, 'damaged', 'APR-015', 2),
('Warehouse forklift impact — boxes crushed',     -3, 'damaged', 'APR-016', 2),
('Dye bleed detected during QC scan',             -5, 'damaged', 'APR-017', 2),
('Elastic failure in stored units',               -4, 'damaged', 'APR-018', 2),
('Stitching defect on received shipment',         -2, 'damaged', 'APR-019', 2),
('Moisture exposure in storage bay',              -3, 'damaged', 'APR-021', 2),
('Thread pull during repacking',                  -1, 'damaged', 'APR-022', 2),
('Broken buckle hardware on batch',               -5, 'damaged', 'APR-023', 2),
('Wrong wash cycle — items shrunk',               -4, 'damaged', 'APR-025', 2),
('Lining delamination on received lot',           -3, 'damaged', 'APR-026', 2),
('Strap tearing on multiple units',               -6, 'damaged', 'APR-027', 2),
('Color irregularity found during QC',            -2, 'damaged', 'APR-029', 2),
('Sole separation on footwear batch',             -5, 'damaged', 'APR-030', 2),
('Oxidation staining on metal hardware',          -3, 'damaged', 'APR-031', 2),
('Nylon pilling beyond acceptable grade',         -4, 'damaged', 'APR-033', 2),
('Transit compression flattened collars',         -2, 'damaged', 'APR-034', 2),
('Seam rip on robe samples',                      -3, 'damaged', 'APR-038', 2),
('Drawstring fraying in bulk lot',                -4, 'damaged', 'APR-039', 2),
('Fleece pilling on entire received batch',       -6, 'damaged', 'APR-040', 2),
('Ink transfer staining during packing',          -2, 'damaged', 'APR-037', 2),

-- ── CORRECTION (30 rows) ──────────────────────────────────────────────────
('Recount after annual audit — units found',      +5, 'correction', 'APR-001', 2),
('Inventory discrepancy resolved after recount',  -2, 'correction', 'APR-002', 2),
('Miscount corrected from barcode scan',          +3, 'correction', 'APR-004', 2),
('Returns processed back into stock',             +4, 'correction', 'APR-005', 2),
('System sync error fixed — qty adjusted',        -1, 'correction', 'APR-006', 2),
('Found hidden units in overflow storage',        +6, 'correction', 'APR-008', 2),
('Wrong bin scanned during pick — corrected',     -3, 'correction', 'APR-009', 1),
('Manual recount post-cycle count',               +2, 'correction', 'APR-010', 2),
('Data entry error corrected',                    -4, 'correction', 'APR-011', 1),
('Units found behind shelving during audit',      +5, 'correction', 'APR-012', 2),
('Mis-shipped items returned and restocked',      +3, 'correction', 'APR-013', 2),
('Shopify sync discrepancy resolved',             -2, 'correction', 'APR-015', 2),
('Recount after supplier dispute settled',        +8, 'correction', 'APR-016', 2),
('QC hold released — items back in stock',        +4, 'correction', 'APR-017', 3),
('Transfer from secondary warehouse complete',    +7, 'correction', 'APR-018', 2),
('Cycle count correction — overage found',        -3, 'correction', 'APR-019', 2),
('Barcode mis-read corrected in system',          +2, 'correction', 'APR-020', 2),
('Restock from cancelled order',                  +5, 'correction', 'APR-021', 2),
('Found mislabeled box in back storage',          +4, 'correction', 'APR-022', 1),
('Belt units reallocated from archived SKU',      +3, 'correction', 'APR-023', 2),
('Return from retail partner processed',          +6, 'correction', 'APR-025', 2),
('Recount correction from third-party audit',     -2, 'correction', 'APR-026', 2),
('Replacement units received for recall',         +5, 'correction', 'APR-027', 2),
('Quantity adjusted after photo-shoot sample use',-1, 'correction', 'APR-029', 3),
('Recount after SKU merge resolved',              +3, 'correction', 'APR-030', 2),
('Found misplaced shipment in receiving dock',    +9, 'correction', 'APR-031', 2),
('Restock after photoshoot — samples returned',   +2, 'correction', 'APR-033', 2),
('Cycle count — slight overage corrected',        -1, 'correction', 'APR-037', 2),
('Units found during packing station sweep',      +4, 'correction', 'APR-039', 2),
('Recount resolved mismatch from Shopify export', -2, 'correction', 'APR-040', 2);