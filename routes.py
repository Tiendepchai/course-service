from flask import Blueprint, request, jsonify
from database import get_db_connection

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course_db")
    courses = cursor.fetchall()
    conn.close()
    return jsonify(courses)

@course_bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM course_db WHERE id = %s", (id,))
    course = cursor.fetchone()
    conn.close()
    if course:
        return jsonify(course)
    return jsonify({'error': 'course not found'}), 404

@course_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO course_db (name, description) VALUES (%s, %s)", 
                   (data['name'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'course created successfully'}), 201

@course_bp.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE course_db SET name = %s, description = %s WHERE id = %s",
                   (data['name'], data['description'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'course updated successfully'})

@course_bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course_db WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'course deleted successfully'})
