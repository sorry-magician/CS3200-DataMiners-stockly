# analytics.py
# Flask Blueprint — Analytics domain
# Serves Priya Nair (Business Analyst) — Persona 3


from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import get_db

# Register the Blueprint.
# The url_prefix '/api' is set in __init__.py,
# so every route here is accessible at /api/...

analytics = Blueprint('analytics', __name__)



# ROUTE 1 — GET /analytics/revenue
# Returns total revenue, order count, and units
# sold aggregated by day for a given date range.
# Accepts optional query params: start_date,
# end_date (format: YYYY-MM-DD). Defaults to
# the last 90 days if params are not provided.
# User Story: Priya-1

@analytics.route('/analytics/revenue', methods=['GET'])
def get_revenue_trends():
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')

    cursor = get_db().cursor()

    # If both date params are supplied, filter
    # by the explicit range; otherwise default
    # to the last 90 days.
    if start_date and end_date:
        query = '''
            SELECT  so.order_date,
                    COUNT(DISTINCT so.order_id)              AS total_orders,
                    SUM(sop.quantity_sold)                   AS total_units_sold,
                    SUM(sop.quantity_sold
                        * sop.unit_price_at_sale)            AS total_revenue
            FROM    Sales_Orders so
                JOIN Sales_Order_Products sop
                    ON so.order_id = sop.order_id
            WHERE   so.order_date BETWEEN %s AND %s
            GROUP BY so.order_date
            ORDER BY so.order_date ASC
        '''
        cursor.execute(query, (start_date, end_date))
    else:
        query = '''
            SELECT  so.order_date,
                    COUNT(DISTINCT so.order_id)              AS total_orders,
                    SUM(sop.quantity_sold)                   AS total_units_sold,
                    SUM(sop.quantity_sold
                        * sop.unit_price_at_sale)            AS total_revenue
            FROM    Sales_Orders so
                JOIN Sales_Order_Products sop
                    ON so.order_id = sop.order_id
            WHERE   DATEDIFF(CURDATE(), so.order_date) <= 90
            GROUP BY so.order_date
            ORDER BY so.order_date ASC
        '''
        cursor.execute(query)

    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 2 — GET /analytics/category_performance
# Returns revenue, units sold, order count, and
# average selling price broken down by product
# category. Excludes archived products.
# User Story: Priya-2

@analytics.route('/analytics/category_performance', methods=['GET'])
def get_category_performance():
    cursor = get_db().cursor()
    query = '''
        SELECT  c.category_name,
                COUNT(DISTINCT so.order_id)              AS total_orders,
                SUM(sop.quantity_sold)                   AS total_units_sold,
                SUM(sop.quantity_sold
                    * sop.unit_price_at_sale)            AS total_revenue,
                AVG(sop.unit_price_at_sale)              AS avg_selling_price
        FROM    Sales_Order_Products sop
            JOIN Products p
                ON sop.sku = p.sku
            JOIN Categories c
                ON p.category_id = c.category_id
            JOIN Sales_Orders so
                ON sop.order_id = so.order_id
        WHERE   p.is_archived = FALSE
        GROUP BY c.category_name
        ORDER BY total_revenue DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 3 — GET /analytics/sell_through
# Returns the sell-through rate per SKU over
# the last 90 days.
# Formula: units_sold / (units_sold + qty_on_hand)
# expressed as a percentage.
# Accepts optional query param: days (int,
# defaults to 90). Allows Priya to switch
# between 30 / 60 / 90 day windows from the UI.
# User Story: Priya-3

@analytics.route('/analytics/sell_through', methods=['GET'])
def get_sell_through():
    days = request.args.get('days', 90)

    cursor = get_db().cursor()
    query = '''
        SELECT  p.sku,
                p.product_name,
                c.category_name,
                COALESCE(SUM(sop.quantity_sold), 0)
                    AS units_sold,
                p.quantity_on_hand              AS current_stock,
                COALESCE(
                    SUM(sop.quantity_sold) * 100.0
                    / NULLIF(
                        SUM(sop.quantity_sold) + p.quantity_on_hand,
                        0
                    ),
                    0
                )                               AS sell_through_rate_pct
        FROM    Products p
            JOIN Categories c
                ON p.category_id = c.category_id
            LEFT JOIN Sales_Order_Products sop
                ON p.sku = sop.sku
            LEFT JOIN Sales_Orders so
                ON sop.order_id = so.order_id
                AND DATEDIFF(CURDATE(), so.order_date) <= %s
        WHERE   p.is_archived = FALSE
        GROUP BY p.sku,
                 p.product_name,
                 c.category_name,
                 p.quantity_on_hand
        ORDER BY sell_through_rate_pct DESC
    '''
    cursor.execute(query, (days,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 4 — GET /analytics/turnover
# Returns inventory turnover ratio per product.
# Formula: total_units_sold / qty_on_hand
# A higher ratio indicates faster-moving stock.
# Products with zero stock are excluded via
# NULLIF to avoid division-by-zero.
# User Story: Priya-4

@analytics.route('/analytics/turnover', methods=['GET'])
def get_turnover():
    cursor = get_db().cursor()
    query = '''
        SELECT  p.sku,
                p.product_name,
                c.category_name,
                COALESCE(SUM(sop.quantity_sold), 0)
                    AS total_units_sold,
                p.quantity_on_hand,
                COALESCE(
                    SUM(sop.quantity_sold) * 1.0
                    / NULLIF(p.quantity_on_hand, 0),
                    0
                )                               AS turnover_ratio
        FROM    Products p
            JOIN Categories c
                ON p.category_id = c.category_id
            LEFT JOIN Sales_Order_Products sop
                ON p.sku = sop.sku
        WHERE   p.is_archived = FALSE
        GROUP BY p.sku,
                 p.product_name,
                 c.category_name,
                 p.quantity_on_hand
        ORDER BY turnover_ratio DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 5 — GET /analytics/supplier_lead_times
# Returns each active supplier with their stated
# lead time, number of products supplied, and
# total / average stock held for those products.
# Used by Priya to identify which suppliers
# carry the most inventory weight and whether
# their lead times are competitive.
# User Story: Priya-6

@analytics.route('/analytics/supplier_lead_times', methods=['GET'])
def get_supplier_lead_times():
    cursor = get_db().cursor()
    query = '''
        SELECT  s.supplier_name,
                s.lead_time_days,
                COUNT(DISTINCT ps.sku)          AS products_supplied,
                SUM(p.quantity_on_hand)         AS total_stock_supplied,
                AVG(p.quantity_on_hand)         AS avg_stock_per_product
        FROM    Suppliers s
            JOIN Product_Suppliers ps
                ON s.supplier_id = ps.supplier_id
            JOIN Products p
                ON ps.sku = p.sku
        WHERE   s.is_active = TRUE
            AND p.is_archived = FALSE
        GROUP BY s.supplier_id,
                 s.supplier_name,
                 s.lead_time_days
        ORDER BY s.lead_time_days ASC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

