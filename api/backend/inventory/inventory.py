from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

inventory = Blueprint('inventory', __name__)

@inventory.route('/purchase_orders', methods=['GET'])
def get_all_purchase_orders():
    cursor = db.get_db().cursor()
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