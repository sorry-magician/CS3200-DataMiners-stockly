from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import get_db

inventory = Blueprint('inventory', __name__)

@inventory.route('/purchase_orders', methods=['GET'])
def get_all_purchase_orders():
    cursor = get_db().cursor()
    query = '''
        SELECT  po.po_id,
                po.order_date,
                po.expected_delivery_date,
                po.status,
                po.notes,
                s.supplier_name,
                u.full_name AS ordered_by
        FROM    Purchase_Orders po
        JOIN    Suppliers s ON po.supplier_id = s.supplier_id
        JOIN    Users     u ON po.user_id     = u.user_id
        ORDER BY po.order_date DESC
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


@inventory.route('/purchase_orders', methods=['POST'])
def create_purchase_order():
    body                   = request.get_json()
    supplier_name          = body['supplier_name']
    expected_delivery_date = body['expected_delivery_date']
    notes                  = body.get('notes', '')
    user_email             = body['user_email']
    items                  = body['items']   # list of {sku, quantity_ordered}

    conn   = get_db()
    cursor = conn.cursor()

    # Step 1 — Insert PO header
    header_query = '''
        INSERT INTO Purchase_Orders
            (order_date, expected_delivery_date, status, notes,
             supplier_id, user_id)
        VALUES (
            CURDATE(),
            %s,
            'ordered',
            %s,
            (SELECT supplier_id FROM Suppliers WHERE supplier_name = %s),
            (SELECT user_id     FROM Users     WHERE email         = %s)
        )
    '''
    cursor.execute(header_query,
                   (expected_delivery_date, notes, supplier_name, user_email))
    po_id = cursor.lastrowid

    # Step 2 — Insert each product line item
    item_query = '''
        INSERT INTO PO_Products (sku, po_id, quantity_ordered)
        VALUES (%s, %s, %s)
    '''
    for item in items:
        cursor.execute(item_query,
                       (item['sku'], po_id, item['quantity_ordered']))

    conn.commit()
    return make_response(
        jsonify({'message': 'Purchase order created successfully',
                 'po_id': po_id}),
        201
    )

@inventory.route('/purchase_orders/<int:po_id>', methods=['GET'])
def get_purchase_order(po_id):
    cursor = get_db().cursor()
    query = '''
        SELECT  po.po_id,
                po.order_date,
                po.expected_delivery_date,
                po.status,
                po.notes,
                s.supplier_name,
                u.full_name        AS ordered_by,
                pp.sku,
                p.product_name,
                pp.quantity_ordered,
                DATEDIFF(po.expected_delivery_date, po.order_date)
                                   AS lead_time_days
        FROM    Purchase_Orders po
        JOIN    Suppliers   s  ON po.supplier_id = s.supplier_id
        JOIN    Users       u  ON po.user_id     = u.user_id
        JOIN    PO_Products pp ON po.po_id        = pp.po_id
        JOIN    Products    p  ON pp.sku          = p.sku
        WHERE   po.po_id = %s
        ORDER BY pp.sku
    '''
    cursor.execute(query, (po_id,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

@inventory.route('/purchase_orders/<int:po_id>', methods=['PUT'])
def update_po_status(po_id):
    body       = request.get_json()
    new_status = body['status']

    conn   = get_db()
    cursor = conn.cursor()
    query = '''
        UPDATE Purchase_Orders
        SET    status  = %s
        WHERE  po_id   = %s
    '''
    cursor.execute(query, (new_status, po_id))
    conn.commit()
    return make_response(
        jsonify({'message': f'PO {po_id} status updated to {new_status}'}),
        200
    )

@inventory.route('/stock_adjustments', methods=['GET'])
def get_stock_adjustments():
    cursor     = get_db().cursor()
    sku_filter = request.args.get('sku')

    base_select = '''
        SELECT  sa.adjustment_id,
                sa.sku,
                p.product_name,
                sa.quantity_delta,
                sa.adjustment_type,
                sa.reason,
                sa.adjusted_at,
                u.full_name AS adjusted_by
        FROM    Stock_Adjustments sa
        JOIN    Products p ON sa.sku     = p.sku
        JOIN    Users    u ON sa.user_id = u.user_id
    '''

    if sku_filter:
        query = base_select + ' WHERE sa.sku = %s ORDER BY sa.adjusted_at DESC'
        cursor.execute(query, (sku_filter,))
    else:
        query = base_select + ' ORDER BY sa.adjusted_at DESC'
        cursor.execute(query)

    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

@inventory.route('/stock_adjustments', methods=['POST'])
def create_stock_adjustment():
    body            = request.get_json()
    sku             = body['sku']
    quantity_delta  = body['quantity_delta']
    adjustment_type = body['adjustment_type']
    reason          = body['reason']
    user_email      = body['user_email']

    conn   = get_db()
    cursor = conn.cursor()
    query = '''
        INSERT INTO Stock_Adjustments
            (reason, quantity_delta, adjustment_type, sku, user_id)
        VALUES (
            %s, %s, %s, %s,
            (SELECT user_id FROM Users WHERE email = %s)
        )
    '''
    cursor.execute(query,
                   (reason, quantity_delta, adjustment_type, sku, user_email))
    conn.commit()
    return make_response(
        jsonify({'message': 'Stock adjustment logged successfully'}), 201
    )


@inventory.route('/inventory/search', methods=['GET'])
def search_products():
    cursor      = get_db().cursor()
    category_id = request.args.get('category_id')
    supplier_id = request.args.get('supplier_id')

    # Base query — always filters out archived products
    query = '''
        SELECT DISTINCT
               p.sku,
               p.product_name,
               p.quantity_on_hand,
               p.reorder_threshold,
               p.unit_price,
               c.category_name,
               s.supplier_name,
               CASE WHEN p.is_archived = TRUE
                    THEN 'Archived' ELSE 'Active'
               END AS stock_status
        FROM   Products          p
        JOIN   Categories        c  ON p.category_id  = c.category_id
        JOIN   Product_Suppliers ps ON p.sku           = ps.sku
        JOIN   Suppliers         s  ON ps.supplier_id  = s.supplier_id
        WHERE  p.is_archived = FALSE
    '''
    params = []

    if category_id:
        query += ' AND p.category_id = %s'
        params.append(category_id)
    if supplier_id:
        query += ' AND ps.supplier_id = %s'
        params.append(supplier_id)

    query += ' ORDER BY p.product_name'

    if params:
        cursor.execute(query, tuple(params))
    else:
        cursor.execute(query)

    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

@inventory.route('/suppliers', methods=['GET'])
def get_suppliers():
    cursor = get_db().cursor()
    query = '''
        SELECT  supplier_id,
                supplier_name,
                contact_email,
                contact_phone,
                lead_time_days,
                is_active
        FROM    Suppliers
        WHERE   is_active = TRUE
        ORDER BY supplier_name
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

@inventory.route('/suppliers/<int:supplier_id>', methods=['DELETE'])
def deactivate_supplier(supplier_id):
    conn   = get_db()
    cursor = conn.cursor()
    query = '''
        UPDATE Suppliers
        SET    is_active   = FALSE
        WHERE  supplier_id = %s
    '''
    cursor.execute(query, (supplier_id,))
    conn.commit()
    return make_response(
        jsonify({'message': 'Supplier deactivated successfully'}), 200
    )