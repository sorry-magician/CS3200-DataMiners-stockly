DROP DATABASE IF EXISTS stockly_db;
CREATE DATABASE stockly_db;
USE stockly_db;

-- Drop tables in reverse FK dependency order
DROP TABLE IF EXISTS System_Config;
DROP TABLE IF EXISTS Audit_Log;
DROP TABLE IF EXISTS Stock_Adjustments;
DROP TABLE IF EXISTS Sales_Order_Products;
DROP TABLE IF EXISTS Sales_Orders;
DROP TABLE IF EXISTS PO_Products;
DROP TABLE IF EXISTS Purchase_Orders;
DROP TABLE IF EXISTS Product_Suppliers;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;

-- Users
CREATE TABLE Users (
    user_id    INT          AUTO_INCREMENT PRIMARY KEY,
    full_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(150) NOT NULL UNIQUE,
    role       VARCHAR(50)  NOT NULL,
    is_active  BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- Categories
CREATE TABLE Categories (
    category_id   INT          AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

-- Suppliers
CREATE TABLE Suppliers (
    supplier_id    INT          AUTO_INCREMENT PRIMARY KEY,
    supplier_name  VARCHAR(150) NOT NULL,
    contact_email  VARCHAR(150),
    contact_phone  VARCHAR(30),
    is_active      BOOLEAN      NOT NULL DEFAULT TRUE,
    lead_time_days INT
);

-- Products
CREATE TABLE Products (
    sku               VARCHAR(20)   PRIMARY KEY,
    product_name      VARCHAR(150)  NOT NULL,
    description       TEXT,
    unit_price        DECIMAL(10,2) NOT NULL,
    quantity_on_hand  INT           NOT NULL DEFAULT 0,
    reorder_threshold INT           NOT NULL DEFAULT 10,
    is_archived       BOOLEAN       NOT NULL DEFAULT FALSE,
    category_id       INT,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id)
        REFERENCES Categories(category_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- Product_Suppliers (M:N bridge)
CREATE TABLE Product_Suppliers (
    sku         VARCHAR(20) NOT NULL,
    supplier_id INT         NOT NULL,
    PRIMARY KEY (sku, supplier_id),
    CONSTRAINT fk_ps_sku FOREIGN KEY (sku)
        REFERENCES Products(sku)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ps_supplier FOREIGN KEY (supplier_id)
        REFERENCES Suppliers(supplier_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Sales_Orders
CREATE TABLE Sales_Orders (
    order_id   INT      AUTO_INCREMENT PRIMARY KEY,
    order_date DATE     NOT NULL,
    user_id    INT      NOT NULL,
    CONSTRAINT fk_so_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Sales_Order_Products (M:N bridge)
CREATE TABLE Sales_Order_Products (
    order_id          INT           NOT NULL,
    sku               VARCHAR(20)   NOT NULL,
    quantity_sold     INT           NOT NULL,
    unit_price_at_sale DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, sku),
    CONSTRAINT fk_sop_order FOREIGN KEY (order_id)
        REFERENCES Sales_Orders(order_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_sop_sku FOREIGN KEY (sku)
        REFERENCES Products(sku)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Purchase_Orders
CREATE TABLE Purchase_Orders (
    po_id                  INT  AUTO_INCREMENT PRIMARY KEY,
    order_date             DATE NOT NULL,
    expected_delivery_date DATE,
    status                 ENUM('ordered', 'in_transit', 'received') DEFAULT 'ordered',
    notes                  TEXT,
    supplier_id            INT  NOT NULL,
    user_id                INT  NOT NULL,
    CONSTRAINT fk_po_supplier FOREIGN KEY (supplier_id)
        REFERENCES Suppliers(supplier_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_po_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- PO_Products (M:N bridge)
CREATE TABLE PO_Products (
    sku              VARCHAR(20) NOT NULL,
    po_id            INT         NOT NULL,
    quantity_ordered INT         NOT NULL,
    PRIMARY KEY (sku, po_id),
    CONSTRAINT fk_pop_sku FOREIGN KEY (sku)
        REFERENCES Products(sku)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_pop_po FOREIGN KEY (po_id)
        REFERENCES Purchase_Orders(po_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Stock_Adjustments
CREATE TABLE Stock_Adjustments (
    adjustment_id   INT          AUTO_INCREMENT PRIMARY KEY,
    reason          TEXT,
    quantity_delta  INT          NOT NULL,
    adjustment_type ENUM('damaged', 'correction') NOT NULL,
    adjusted_at     DATETIME     DEFAULT CURRENT_TIMESTAMP,
    sku             VARCHAR(20)  NOT NULL,
    user_id         INT          NOT NULL,
    CONSTRAINT fk_adj_sku FOREIGN KEY (sku)
        REFERENCES Products(sku)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_adj_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Audit_Log
CREATE TABLE Audit_Log (
    log_id      INT          AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(100) NOT NULL,
    table_name  VARCHAR(100),
    record_ref  VARCHAR(100),
    changed_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    is_flagged  BOOLEAN      NOT NULL DEFAULT FALSE,
    user_id     INT          NOT NULL,
    CONSTRAINT fk_log_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- System_Config
CREATE TABLE System_Config (
    config_key   VARCHAR(100) PRIMARY KEY,
    config_value VARCHAR(255) NOT NULL,
    updated_at   DATETIME     DEFAULT CURRENT_TIMESTAMP,
    user_id      INT,
    CONSTRAINT fk_config_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

-- Sample Data

INSERT INTO Users (full_name, email, role, is_active) VALUES
    ('Maya Chen',    'maya@stockly.com',   'manager',  TRUE),
    ('Jordan Patel', 'jordan@stockly.com', 'editor',   TRUE),
    ('Priya Nair',   'priya@stockly.com',  'viewer',   TRUE),
    ('Alex Torres',  'alex@stockly.com',   'admin',    TRUE);

INSERT INTO Categories (category_name) VALUES
    ('Bags'),
    ('Tops'),
    ('Outerwear'),
    ('Accessories');

INSERT INTO Suppliers (supplier_name, contact_email, contact_phone, is_active, lead_time_days) VALUES
    ('GreenWeave Co.', 'orders@greenweave.com', '555-1000', TRUE,  7),
    ('EcoFabrics Inc.','hello@ecofabrics.com',  '555-2000', TRUE, 14);

INSERT INTO Products (sku, product_name, description, unit_price, quantity_on_hand, reorder_threshold, is_archived, category_id) VALUES
    ('APR-001', 'Linen Tote Bag',        'Sustainable linen tote',   34.99,  4, 10, FALSE, 1),
    ('APR-047', 'Recycled Denim Jacket', '100% recycled denim',      89.99, 22,  5, FALSE, 3),
    ('APR-022', 'Cotton Cross-Body Bag', 'Organic cotton bag',       44.99, 11, 15, FALSE, 1);

INSERT INTO Product_Suppliers (sku, supplier_id) VALUES
    ('APR-001', 1),
    ('APR-047', 2),
    ('APR-022', 1);

INSERT INTO Sales_Orders (order_date, user_id) VALUES
    ('2026-01-15', 1),
    ('2026-02-03', 1),
    ('2026-03-10', 1);

INSERT INTO Sales_Order_Products (order_id, sku, quantity_sold, unit_price_at_sale) VALUES
    (1, 'APR-001', 12, 34.99),
    (2, 'APR-047',  5, 89.99),
    (3, 'APR-022',  8, 44.99);

INSERT INTO Purchase_Orders (order_date, expected_delivery_date, status, notes, supplier_id, user_id) VALUES
    ('2026-03-01', '2026-04-25', 'in_transit', 'Reorder after low stock alert', 1, 2),
    ('2026-03-15', '2026-05-01', 'ordered',    NULL,                            2, 2);

INSERT INTO PO_Products (sku, po_id, quantity_ordered) VALUES
    ('APR-001', 1, 100),
    ('APR-047', 2,  50);

INSERT INTO Stock_Adjustments (reason, quantity_delta, adjustment_type, sku, user_id) VALUES
    ('Water damage during storage', -2, 'damaged',    'APR-001', 2),
    ('Recount after audit',          5, 'correction', 'APR-022', 2);

INSERT INTO Audit_Log (action_type, table_name, record_ref, is_flagged, user_id) VALUES
    ('UPDATE', 'Products',         'APR-001', FALSE, 2),
    ('INSERT', 'Products',         'APR-047', FALSE, 1),
    ('UPDATE', 'Stock_Adjustments','APR-022', TRUE,  1);

INSERT INTO System_Config (config_key, config_value, user_id) VALUES
    ('low_stock_default', '10',              4),
    ('currency',          'USD',             4),
    ('timezone',          'America/New_York',4);
