from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import pymysql
import config
import re

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

def get_db_connection():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db=config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def validate_reimbursement_data(data):
    required_fields = ["description", "amount", "request_date"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        return False, "Amount must be a positive number"

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if not date_pattern.match(data["request_date"]):
        return False, "Invalid date format. Use YYYY-MM-DD"

    return True, ""

@app.route('/reimbursements', methods=['POST'])
@jwt_required()
def create_reimbursement():
    current_user = get_jwt_identity()
    user_id = current_user['id']
    data = request.json

    is_valid, error_message = validate_reimbursement_data(data)
    if not is_valid:
        return jsonify({"msg": error_message}), 400

    description = data['description']
    amount = data['amount']
    request_date = data['request_date']

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO reimbursements (user_id, description, amount, request_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, description, amount, request_date))
            connection.commit()
            return jsonify({"msg": "Reimbursement request created successfully"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

@app.route('/reimbursements', methods=['GET'])
@jwt_required()
def get_reimbursements():
    current_user = get_jwt_identity()
    user_id = current_user['id']

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM reimbursements"
            if current_user['role'] != "Gerente":
                sql += f" WHERE user_id={user_id}"
            cursor.execute(sql)
            reimbursements = cursor.fetchall()
            return jsonify(reimbursements), 200
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

@app.route('/reimbursements/<int:reimbursement_id>/approve', methods=['PUT'])
@jwt_required()
def approve_reimbursement(reimbursement_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'Gerente':
        return jsonify({"msg": "Permission denied"}), 403

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE reimbursements SET status='Approved', approval_date=NOW() WHERE id=%s"
            cursor.execute(sql, (reimbursement_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({"msg": "Reimbursement approved"}), 200
            else:
                return jsonify({"msg": "Reimbursement not found"}), 404
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

@app.route('/reimbursements/<int:reimbursement_id>/reject', methods=['PUT'])
@jwt_required()
def reject_reimbursement(reimbursement_id):
    current_user = get_jwt_identity()

    if current_user['role'] != 'Gerente':
        return jsonify({"msg": "Permission denied"}), 403

    rejection_reason = request.json.get('rejection_reason')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE reimbursements SET status='Rejected', rejection_reason=%s, approval_date=NOW() WHERE id=%s"
            cursor.execute(sql, (rejection_reason, reimbursement_id))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({"msg": "Reimbursement rejected"}), 200
            else:
                return jsonify({"msg": "Reimbursement not found"}), 404
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

@app.route('/reports/total_by_status', methods=['GET'])
@jwt_required()
def get_total_by_status():
    current_user = get_jwt_identity()

    if current_user['role'] != 'Gerente':
        return jsonify({"msg": "Permission denied"}), 403

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT 
                status, COUNT(*) as count, SUM(amount) as total_amount 
            FROM 
                reimbursements 
            GROUP BY 
                status
            """
            cursor.execute(sql)
            report = cursor.fetchall()
            return jsonify(report), 200
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

@app.route('/reports/total_by_period', methods=['GET'])
@jwt_required()
def get_total_by_period():
    current_user = get_jwt_identity()

    if current_user['role'] != 'Gerente':
        return jsonify({"msg": "Permission denied"}), 403

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"msg": "Start date and end date are required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT 
                request_date, COUNT(*) as count, SUM(amount) as total_amount 
            FROM 
                reimbursements 
            WHERE 
                request_date BETWEEN %s AND %s
            GROUP BY 
                request_date
            """
            cursor.execute(sql, (start_date, end_date))
            report = cursor.fetchall()
            return jsonify(report), 200
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
