# admin.py
# Flask Blueprint — Admin domain
# Serves Alex Torres (System Administrator)

from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import get_db

admin = Blueprint('admin', __name__)


# ROUTE 1 — GET /users
# Returns all users with role and active status.
# User Story: Alex-1, Alex-5
@admin.route('/users', methods=['GET'])
def get_all_users():
    cursor = get_db().cursor()
    query = '''
        SELECT  user_id,
                full_name,
                email,
                role,
                is_active,
                created_at
        FROM    Users
        ORDER BY full_name
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)



# ROUTE 2 — POST /users
# Adds a new user with a specified role.
# User Story: Alex-1
@admin.route('/users', methods=['POST'])
def add_user():
    body      = request.get_json()
    full_name = body['full_name']
    email     = body['email']
    role      = body['role']

    conn   = get_db()
    cursor = conn.cursor()
    query  = '''
        INSERT INTO Users (full_name, email, role, is_active)
        VALUES (%s, %s, %s, TRUE)
    '''
    cursor.execute(query, (full_name, email, role))
    conn.commit()
    return make_response(
        jsonify({'message': 'User added successfully'}), 201
    )


# ROUTE 3 — GET /users/<user_id>
# Returns detail for one user.
# User Story: Alex-5
@admin.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = get_db().cursor()
    query  = '''
        SELECT  user_id,
                full_name,
                email,
                role,
                is_active,
                created_at
        FROM    Users
        WHERE   user_id = %s
    '''
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# ROUTE 4 — PUT /users/<user_id>
# Updates a user's full_name, email, and role.
# User Story: Alex-5
@admin.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    body      = request.get_json()
    full_name = body['full_name']
    email     = body['email']
    role      = body['role']

    conn   = get_db()
    cursor = conn.cursor()
    query  = '''
        UPDATE  Users
        SET     full_name = %s,
                email     = %s,
                role      = %s
        WHERE   user_id   = %s
    '''
    cursor.execute(query, (full_name, email, role, user_id))
    conn.commit()
    return make_response(
        jsonify({'message': 'User updated successfully'}), 200
    )


# ROUTE 5 — PUT /users/<user_id>/deactivate
# Sets is_active = FALSE for a user.
# User Story: Alex-2
@admin.route('/users/<int:user_id>/deactivate', methods=['PUT'])
def deactivate_user(user_id):
    conn   = get_db()
    cursor = conn.cursor()
    query  = '''
        UPDATE  Users
        SET     is_active = FALSE
        WHERE   user_id   = %s
    '''
    cursor.execute(query, (user_id,))
    conn.commit()
    return make_response(
        jsonify({'message': 'User deactivated successfully'}), 200
    )


# ROUTE 6 — GET /audit_log
# Returns audit log entries, optionally filtered.
# User Story: Alex-3
@admin.route('/audit_log', methods=['GET'])
def get_audit_log():
    cursor     = get_db().cursor()
    is_flagged = request.args.get('is_flagged')
    table_name = request.args.get('table_name')

    query = '''
        SELECT  al.log_id,
                al.action_type,
                al.table_name,
                al.record_ref,
                al.changed_at,
                al.is_flagged,
                u.full_name AS changed_by
        FROM    Audit_Log al
            JOIN Users u ON al.user_id = u.user_id
    '''
    params = []

    conditions = []
    if is_flagged is not None:
        conditions.append('al.is_flagged = %s')
        params.append(int(is_flagged))
    if table_name:
        conditions.append('al.table_name = %s')
        params.append(table_name)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    query += ' ORDER BY al.changed_at DESC'

    if params:
        cursor.execute(query, tuple(params))
    else:
        cursor.execute(query)

    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# ROUTE 7 — GET /system_config
# Returns all system config key-value pairs.
# User Story: Alex-4
@admin.route('/system_config', methods=['GET'])
def get_system_config():
    cursor = get_db().cursor()
    query  = '''
        SELECT  config_key,
                config_value,
                updated_at
        FROM    System_Config
        ORDER BY config_key
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)


# ROUTE 8 — PUT /system_config/<config_key>
# Updates the value of a config setting.
# User Story: Alex-4
@admin.route('/system_config/<config_key>', methods=['PUT'])
def update_system_config(config_key):
    body         = request.get_json()
    config_value = body['config_value']

    conn   = get_db()
    cursor = conn.cursor()
    query  = '''
        UPDATE  System_Config
        SET     config_value = %s,
                updated_at   = CURRENT_TIMESTAMP
        WHERE   config_key   = %s
    '''
    cursor.execute(query, (config_value, config_key))
    conn.commit()
    return make_response(
        jsonify({'message': f'Config {config_key} updated successfully'}),
        200
    )


# ROUTE 9 — DELETE /products/<sku>/flag
# Hard deletes a flagged duplicate product.
# Only works if product has no FK dependents.
# User Story: Alex-6
@admin.route('/products/<sku>/flag', methods=['DELETE'])
def delete_flagged_product(sku):
    conn   = get_db()
    cursor = conn.cursor()
    query  = '''
        DELETE FROM Products
        WHERE  sku = %s
        AND    is_archived = TRUE
    '''
    cursor.execute(query, (sku,))
    conn.commit()
    return make_response(
        jsonify({'message': f'Product {sku} permanently deleted'}), 200
    )