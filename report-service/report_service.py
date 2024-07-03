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
                description, amount, request_date, status
            FROM 
                reimbursements 
            WHERE 
                request_date BETWEEN %s AND %s
            
                
            """
            cursor.execute(sql, (start_date, end_date))
            report = cursor.fetchall()
            return jsonify(report), 200
    except pymysql.MySQLError as e:
        return jsonify({"msg": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
