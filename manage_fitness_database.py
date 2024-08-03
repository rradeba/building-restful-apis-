from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError  
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

# Schema for member 
class MemberSchema(ma.Schema): 
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "phone")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Schema for session
class SessionSchema(ma.Schema): 
    time = fields.String(required=True)
    date = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("time", "date", "activity")

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

# MySQL connection data 
db_name = "fitness_db"
user = "root"
password = "843RnR$$"
host = "127.0.0.1"
port = 3306  

def get_db_connection():
    try:          
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# POST method for members
@app.route('/members', methods=['POST'])
def add_member():
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e: 
        print(f"Error: {e}")
        return jsonify(e.messages), 400 

    try: 
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        new_member = (member_data['name'], member_data['email'], member_data['phone'])
        query = "INSERT INTO members (name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, new_member)
        conn.commit()
        return jsonify({"message": "Member added successfully"}), 201
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# GET method for members
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:  
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"}), 404
        else:
            return member_schema.jsonify(member)
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# PUT method for members
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):   
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e: 
        print(f"Error: {e}")
        return jsonify(e.messages), 400 

    try: 
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        updated_member = (member_data['name'], member_data['email'], member_data['phone'], id)
        query = "UPDATE members SET name = %s, email = %s, phone = %s WHERE id = %s"
        cursor.execute(query, updated_member)
        conn.commit()
        return jsonify({"message": "Member updated successfully"}), 200
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# DELETE method for members
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try: 
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"}), 404

        query = "DELETE FROM members WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return jsonify({"message": "Member removed successfully"}), 200
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# POST method for sessions 
@app.route('/workoutsessions', methods=['POST'])
def schedule_session():
    try: 
        session_data = session_schema.load(request.json)
    except ValidationError as e: 
        print(f"Error: {e}")
        return jsonify(e.messages), 400 

    try: 
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        new_session = (session_data['time'], session_data['date'], session_data['activity'])
        query = "INSERT INTO workoutsessions (time, date, activity) VALUES (%s, %s, %s)"
        cursor.execute(query, new_session)
        conn.commit()
        return jsonify({"message": "Session scheduled successfully"}), 201
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# GET method for sessions
@app.route('/workoutsessions/<int:id>', methods=['GET'])
def get_session(id):
    try:  
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workoutsessions WHERE id = %s", (id,))
        session = cursor.fetchone()
        if not session:
            return jsonify({"error": "Session not found"}), 404
        else:
            return session_schema.jsonify(session)
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# PUT method for sessions
@app.route('/workoutsessions/<int:id>', methods=['PUT'])
def update_session(id):   
    try: 
        session_data = session_schema.load(request.json)
    except ValidationError as e: 
        print(f"Error: {e}")
        return jsonify(e.messages), 400 

    try: 
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        updated_session = (session_data['time'], session_data['date'], session_data['activity'], id)
        query = "UPDATE workoutsessions SET time = %s, date = %s, activity = %s WHERE id = %s"
        cursor.execute(query, updated_session)
        conn.commit()
        return jsonify({"message": "Session updated successfully"}), 200
    except Error as e: 
        print(f"Error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)



    