# Stockly — CS 3200 Spring 2026

### Team: Data Miners

## Team Members
- Arnav Agarwal — agarwal.arna@northeastern.edu
- Krishna Jhangimal — jhangimal.k@northeastern.edu
- Spencer Li — li.sp@northeastern.edu

## Demo Video
[INSERT YOUTUBE LINK HERE]

## GitHub Repository
[INSERT GITHUB REPO LINK HERE]

## Project Overview
Stockly is an inventory management platform built for small e-commerce
businesses that have outgrown spreadsheets. It centralizes product inventory,
sales data, supplier records, and business analytics into one data-driven
dashboard. Stockly serves four types of users — store owners who need
real-time inventory visibility, inventory managers who track purchase orders
and stock adjustments, business analysts who need sales performance dashboards,
and system administrators who manage users and system configuration.

## Tech Stack
- **Database:** MySQL 9
- **API:** Python Flask with Blueprints
- **Frontend:** Streamlit
- **Infrastructure:** Docker and docker-compose

## Project Structure
api/
backend/
products/              Store Owner blueprint (Maya Chen)
inventory/             Inventory Manager blueprint (Jordan Patel)
analytics/             Business Analyst blueprint (Priya Nair)
admin/                 System Admin blueprint (Alex Torres)
db_connection/         MySQL connection handler
rest_entry.py            App factory and blueprint registration
backend_app.py           Entry point
app/src/
pages/                   One file per page per persona
modules/nav.py           Role-based sidebar navigation
Home.py                  Login and persona selection page
database-files/
01_ddl.sql               Database schema (12 tables)
02_data.sql              Users, Categories, Products seed data
04_data_inventory.sql    Suppliers, Purchase Orders, Stock Adjustments
05_sales_orders.sql      Sales Orders seed data
06_sales_order_products.sql  Sales Order Products seed data

## Getting Started

### Prerequisites
- Docker Desktop installed and running
- Git

### Setup

**Step 1 — Clone the repository:**
https://github.com/sorry-magician/CS3200-DataMiners-stockly.git

**Step 2 — Create the `.env` file inside the `api/` folder.**

Create a file named `.env` inside the `api/` directory with the
following contents:
SECRET_KEY=stockly-secret-key-cs3200
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=stockly_db
MYSQL_ROOT_PASSWORD=stockly1234

**Step 3 — Start all containers:**
**Step 4 — Access the application:**
- Streamlit UI: http://localhost:8501
- Flask API: http://localhost:4000

### Stopping the App

### Resetting the Database

## User Personas
| Persona | Role | Pages |
| Maya Chen | Store Owner | Inventory Dashboard, Product Management, Overstock Analysis |
| Jordan Patel | Inventory Manager | Purchase Orders, Inventory Search, Stock Management |
| Priya Nair | Business Analyst | Revenue Dashboard, Product Performance, Supplier Analysis |
| Alex Torres | System Administrator | User Management, Audit Log, System Config |

## API Blueprints

### Products — Maya Chen (Store Owner)
| Method | Route | Description |
| GET | /products | All active products |
| POST | /products | Add a new product |
| GET | /products/low-stock | Products below reorder threshold |
| GET | /products/overstock | Overstocked products using 90 day sales history |
| GET | /categories | All product categories |
| GET | /products/<sku> | Single product detail |
| PUT | /products/<sku> | Update price and reorder threshold |
| DELETE | /products/<sku> | Archive a product (soft delete) |

### Inventory — Jordan Patel (Inventory Manager)
| Method | Route | Description |
| GET | /purchase_orders | All purchase orders |
| POST | /purchase_orders | Create a purchase order |
| GET | /purchase_orders/<id> | Single PO detail with line items |
| PUT | /purchase_orders/<id> | Update PO status |
| GET | /stock_adjustments | All stock adjustments |
| POST | /stock_adjustments | Log a stock adjustment |
| GET | /inventory/search | Search products by category and supplier |
| GET | /suppliers | All active suppliers |
| DELETE | /suppliers/<id> | Deactivate a supplier |

### Analytics — Priya Nair (Business Analyst)
| Method | Route | Description |
| GET | /analytics/revenue | Monthly revenue for a date range |
| GET | /analytics/category_performance | Revenue and units by category |
| GET | /analytics/sell_through | Sell-through rate per SKU |
| GET | /analytics/turnover | Inventory turnover rate per product |
| GET | /analytics/supplier_lead_times | Average lead time per supplier |

### Admin — Alex Torres (System Administrator)
| Method | Route | Description |
| GET | /users | All users |
| POST | /users | Add a new user |
| GET | /users/<id> | Single user detail |
| PUT | /users/<id> | Update user information |
| PUT | /users/<id>/deactivate | Deactivate a user account |
| GET | /audit_log | Audit log with optional filters |
| GET | /system_config | All system config settings |
| PUT | /system_config/<key> | Update a config setting |
| DELETE | /products/<sku>/flag | Permanently delete flagged product |