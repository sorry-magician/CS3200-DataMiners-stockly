
# products.py
# Flask Blueprint — Products & Categories domain
# Serves Maya Chen (Store Owner) — Persona 1
# Arnav Agarwal | CS 3200 | Data Miners | Stockly


from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import get_db

# Register the Blueprint.
# The url_prefix '/api' is set in __init__.py,
# so every route here is accessible at /api/...

products = Blueprint('products', __name__)



# ROUTE 1 — GET /products
# Returns all non-archived products joined
# with their category name.
# User Story: Maya-1

@products.route('/products', methods=['GET'])
def get_all_products():
    cursor = db.get_db().cursor()
    query = '''
        SELECT  p.sku,
                p.product_name,
                p.description,
                p.unit_price,
                p.quantity_on_hand,
                p.reorder_threshold,
                p.is_archived,
                c.category_name
        FROM    Products p
            LEFT JOIN Categories c
                ON p.category_id = c.category_id
        WHERE   p.is_archived = FALSE
        ORDER BY p.product_name
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 2 — POST /products
# Adds a new product to the catalog.
# Accepts JSON body. Looks up category_id
# from category_name — no hardcoding.
# User Story: Maya-2

@products.route('/products', methods=['POST'])
def add_product():
    body              = request.get_json()
    sku               = body['sku']
    product_name      = body['product_name']
    description       = body['description']
    unit_price        = body['unit_price']
    quantity_on_hand  = body['quantity_on_hand']
    reorder_threshold = body['reorder_threshold']
    category_name     = body['category_name']

    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Products
            (sku, product_name, description,
             unit_price, quantity_on_hand,
             reorder_threshold, is_archived, category_id)
        SELECT  %s, %s, %s, %s, %s, %s, FALSE,
                category_id
        FROM    Categories
        WHERE   category_name = %s
    '''
    cursor.execute(query, (sku, product_name, description,
                           unit_price, quantity_on_hand,
                           reorder_threshold, category_name))
    db.get_db().commit()
    return make_response(
        jsonify({'message': 'Product added successfully'}), 201
    )



# ROUTE 3 — GET /products/low-stock
# Returns all non-archived products where
# quantity_on_hand is below reorder_threshold,
# joined with category name and units needed.
#
# !! MUST be defined BEFORE /products/<sku> !!
# If <sku> comes first, Flask matches the string
# 'low-stock' as a SKU and this route is never
# reached.
#
# User Story: Maya-3

@products.route('/products/low-stock', methods=['GET'])
def get_low_stock():
    cursor = db.get_db().cursor()
    query = '''
        SELECT  p.sku,
                p.product_name,
                c.category_name,
                p.quantity_on_hand,
                p.reorder_threshold,
                p.reorder_threshold - p.quantity_on_hand
                    AS units_needed
        FROM    Products p
            JOIN Categories c
                ON p.category_id = c.category_id
        WHERE   p.quantity_on_hand < p.reorder_threshold
            AND p.is_archived = FALSE
        ORDER BY units_needed DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 4 — GET /products/overstock
# Returns non-archived products whose
# quantity_on_hand exceeds reorder_threshold
# AND units sold in the last 90 days is below
# reorder_threshold, using sales history.
#
# !! MUST be defined BEFORE /products/<sku> !!
# Same reason as above.
#
# User Story: Maya-6
# ================================================

@products.route('/products/overstock', methods=['GET'])
def get_overstock():
    cursor = db.get_db().cursor()
    query = '''
        SELECT  p.sku,
                p.product_name,
                p.quantity_on_hand,
                p.reorder_threshold,
                COALESCE(SUM(sop.quantity_sold), 0)
                    AS units_sold_last_90_days
        FROM    Products p
            LEFT JOIN Sales_Order_Products sop
                ON p.sku = sop.sku
            LEFT JOIN Sales_Orders so
                ON sop.order_id = so.order_id
                AND DATEDIFF(CURDATE(), so.order_date) <= 90
        WHERE   p.is_archived = FALSE
        GROUP BY p.sku,
                 p.product_name,
                 p.quantity_on_hand,
                 p.reorder_threshold
        HAVING  p.quantity_on_hand > p.reorder_threshold
            AND COALESCE(SUM(sop.quantity_sold), 0)
                    < p.reorder_threshold
        ORDER BY p.quantity_on_hand DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 5 — GET /categories
# Returns all product categories.
# Used by Maya when adding a product (Maya-2)
# and by Jordan when filtering inventory
# (Jordan-4). Shared resource — cited by both.

@products.route('/categories', methods=['GET'])
def get_categories():
    cursor = db.get_db().cursor()
    query = '''
        SELECT  category_id,
                category_name
        FROM    Categories
        ORDER BY category_name
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 6 — GET /products/<sku>
# Returns full detail for one specific product
# identified by its SKU.
# User Story: Maya-1, Maya-4

@products.route('/products/<sku>', methods=['GET'])
def get_product(sku):
    cursor = db.get_db().cursor()
    query = '''
        SELECT  p.sku,
                p.product_name,
                p.description,
                p.unit_price,
                p.quantity_on_hand,
                p.reorder_threshold,
                p.is_archived,
                c.category_name
        FROM    Products p
            LEFT JOIN Categories c
                ON p.category_id = c.category_id
        WHERE   p.sku = %s
    '''
    cursor.execute(query, (sku,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 7 — PUT /products/<sku>
# Updates unit_price and reorder_threshold
# for the product identified by SKU.
# Accepts JSON body with both fields.
# User Story: Maya-4

@products.route('/products/<sku>', methods=['PUT'])
def update_product(sku):
    body              = request.get_json()
    unit_price        = body['unit_price']
    reorder_threshold = body['reorder_threshold']

    cursor = db.get_db().cursor()
    query = '''
        UPDATE  Products
        SET     unit_price        = %s,
                reorder_threshold = %s
        WHERE   sku = %s
    '''
    cursor.execute(query, (unit_price, reorder_threshold, sku))
    db.get_db().commit()
    return make_response(
        jsonify({'message': 'Product updated successfully'}), 200
    )



# ROUTE 8 — DELETE /products/<sku>
# Soft-deletes a product by setting
# is_archived = TRUE. The product and all its
# historical sales and adjustment data remain
# intact in the database.
# User Story: Maya-5

@products.route('/products/<sku>', methods=['DELETE'])
def archive_product(sku):
    cursor = db.get_db().cursor()
    query = '''
        UPDATE  Products
        SET     is_archived = TRUE
        WHERE   sku = %s
    '''
    cursor.execute(query, (sku,))
    db.get_db().commit()
    return make_response(
        jsonify({'message': 'Product archived successfully'}), 200
    )

