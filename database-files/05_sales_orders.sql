-- 02_sales_orders.sql
-- Mock data for Sales_Orders table
-- 60 rows spread across April 2024 – April 2025
--
-- are assumed to occupy user_id 1–4:
--   1 = Maya Chen (owner)
--   2 = Jordan Patel (inventory)
--   3 = Priya Nair (analyst)  ← most orders reference real users
--   4 = Alex Torres (admin)
--   5–35 = regular customer/staff users


INSERT INTO Sales_Orders (order_id, user_id, order_date, status, notes) VALUES
(1,  12, '2024-04-03', 'completed', NULL),
(2,  7,  '2024-04-11', 'completed', 'Gift wrap requested'),
(3,  19, '2024-04-18', 'completed', NULL),
(4,  25, '2024-04-22', 'cancelled', 'Customer changed mind'),
(5,  3,  '2024-04-29', 'completed', NULL),
(6,  8,  '2024-05-04', 'completed', NULL),
(7,  14, '2024-05-09', 'completed', 'Expedited shipping'),
(8,  31, '2024-05-15', 'completed', NULL),
(9,  6,  '2024-05-20', 'completed', NULL),
(10, 22, '2024-05-27', 'completed', NULL),
(11, 17, '2024-06-02', 'completed', NULL),
(12, 9,  '2024-06-08', 'completed', 'First-time customer'),
(13, 28, '2024-06-14', 'completed', NULL),
(14, 5,  '2024-06-19', 'cancelled', 'Out of stock at time of order'),
(15, 33, '2024-06-25', 'completed', NULL),
(16, 11, '2024-07-01', 'completed', NULL),
(17, 20, '2024-07-07', 'completed', NULL),
(18, 4,  '2024-07-13', 'completed', NULL),
(19, 16, '2024-07-18', 'completed', 'Loyalty discount applied'),
(20, 27, '2024-07-24', 'completed', NULL),
(21, 2,  '2024-07-30', 'completed', NULL),
(22, 13, '2024-08-05', 'completed', NULL),
(23, 35, '2024-08-11', 'completed', NULL),
(24, 10, '2024-08-17', 'completed', NULL),
(25, 24, '2024-08-22', 'completed', 'Back-to-school promo'),
(26, 18, '2024-08-28', 'completed', NULL),
(27, 30, '2024-09-03', 'completed', NULL),
(28, 7,  '2024-09-09', 'completed', NULL),
(29, 23, '2024-09-15', 'completed', NULL),
(30, 15, '2024-09-20', 'cancelled', 'Payment failed'),
(31, 34, '2024-09-26', 'completed', NULL),
(32, 21, '2024-10-02', 'completed', NULL),
(33, 8,  '2024-10-08', 'completed', NULL),
(34, 29, '2024-10-14', 'completed', 'Fall sale order'),
(35, 12, '2024-10-20', 'completed', NULL),
(36, 6,  '2024-10-26', 'completed', NULL),
(37, 19, '2024-11-01', 'completed', NULL),
(38, 26, '2024-11-07', 'completed', NULL),
(39, 3,  '2024-11-13', 'completed', NULL),
(40, 32, '2024-11-19', 'completed', 'Holiday early order'),
(41, 14, '2024-11-25', 'completed', NULL),
(42, 9,  '2024-11-28', 'completed', 'Black Friday order'),
(43, 22, '2024-12-03', 'completed', NULL),
(44, 17, '2024-12-09', 'completed', NULL),
(45, 5,  '2024-12-14', 'completed', 'Holiday gift order'),
(46, 31, '2024-12-19', 'completed', NULL),
(47, 11, '2024-12-24', 'completed', 'Christmas Eve order'),
(48, 27, '2024-12-30', 'completed', NULL),
(49, 20, '2025-01-05', 'completed', NULL),
(50, 4,  '2025-01-11', 'completed', NULL),
(51, 16, '2025-01-17', 'completed', 'New year sale'),
(52, 33, '2025-01-23', 'completed', NULL),
(53, 10, '2025-02-02', 'completed', NULL),
(54, 24, '2025-02-10', 'completed', NULL),
(55, 13, '2025-02-18', 'completed', "Valentine's Day gift"),
(56, 18, '2025-02-26', 'completed', NULL),
(57, 35, '2025-03-05', 'completed', NULL),
(58, 21, '2025-03-13', 'completed', NULL),
(59, 29, '2025-03-21', 'completed', NULL),
(60, 8,  '2025-04-01', 'pending',   'Recently placed');
