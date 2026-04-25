from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def get_payload():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict()


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def fetch_all(query, params=()):
    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_one(query, params=()):
    conn = get_db_connection()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None


@app.route('/')
def index():
    return jsonify({
        'message': 'Simple site with a small SQLite database example',
        'endpoints': [
            'GET /students',
            'POST /students',
            'GET /students/<id>',
            'GET /students/<id>/courses',
            'GET /courses',
            'POST /courses',
            'GET /courses/<id>',
            'GET /enrollments',
            'POST /enrollments'
        ]
    })


@app.route('/students', methods=['GET', 'POST'])
def students():
    conn = get_db_connection()
    if request.method == 'POST':
        data = get_payload()
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            conn.close()
            return jsonify({'error': 'name and email are required'}), 400

        try:
            cursor = conn.execute(
                'INSERT INTO students (name, email) VALUES (?, ?)',
                (name, email),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            conn.close()
            return jsonify({'error': str(exc)}), 400

        student = conn.execute(
            'SELECT id, name, email FROM students WHERE id = ?',
            (cursor.lastrowid,),
        ).fetchone()
        conn.close()
        return jsonify(dict(student)), 201

    students = conn.execute(
        '''
        SELECT
            s.id,
            s.name,
            s.email,
            COUNT(e.id) AS courses_count
        FROM students s
        LEFT JOIN enrollments e ON e.student_id = s.id
        GROUP BY s.id
        ORDER BY s.id
        '''
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])


@app.route('/students/<int:student_id>')
def student_detail(student_id):
    student = fetch_one(
        'SELECT id, name, email FROM students WHERE id = ?',
        (student_id,),
    )
    if not student:
        return jsonify({'error': 'student not found'}), 404

    courses = fetch_all(
        '''
        SELECT
            c.id,
            c.code,
            c.title,
            c.credits,
            e.enrolled_on,
            e.grade
        FROM enrollments e
        JOIN courses c ON c.id = e.course_id
        WHERE e.student_id = ?
        ORDER BY c.code
        ''',
        (student_id,),
    )
    student['courses'] = courses
    return jsonify(student)


@app.route('/students/<int:student_id>/courses')
def student_courses(student_id):
    student = fetch_one('SELECT id FROM students WHERE id = ?', (student_id,))
    if not student:
        return jsonify({'error': 'student not found'}), 404

    return jsonify(fetch_all(
        '''
        SELECT
            c.id,
            c.code,
            c.title,
            c.credits,
            e.enrolled_on,
            e.grade
        FROM enrollments e
        JOIN courses c ON c.id = e.course_id
        WHERE e.student_id = ?
        ORDER BY c.code
        ''',
        (student_id,),
    ))


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    conn = get_db_connection()
    if request.method == 'POST':
        data = get_payload()
        code = data.get('code')
        title = data.get('title')
        credits = to_int(data.get('credits', 3))

        if not code or not title:
            conn.close()
            return jsonify({'error': 'code and title are required'}), 400
        if credits is None:
            conn.close()
            return jsonify({'error': 'credits must be an integer'}), 400

        try:
            cursor = conn.execute(
                'INSERT INTO courses (code, title, credits) VALUES (?, ?, ?)',
                (code, title, credits),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            conn.close()
            return jsonify({'error': str(exc)}), 400

        course = conn.execute(
            'SELECT id, code, title, credits FROM courses WHERE id = ?',
            (cursor.lastrowid,),
        ).fetchone()
        conn.close()
        return jsonify(dict(course)), 201

    courses = conn.execute(
        '''
        SELECT
            c.id,
            c.code,
            c.title,
            c.credits,
            COUNT(e.id) AS students_count
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        GROUP BY c.id
        ORDER BY c.code
        '''
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in courses])


@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = fetch_one(
        'SELECT id, code, title, credits FROM courses WHERE id = ?',
        (course_id,),
    )
    if not course:
        return jsonify({'error': 'course not found'}), 404

    students = fetch_all(
        '''
        SELECT
            s.id,
            s.name,
            s.email,
            e.enrolled_on,
            e.grade
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        WHERE e.course_id = ?
        ORDER BY s.name
        ''',
        (course_id,),
    )
    course['students'] = students
    return jsonify(course)


@app.route('/enrollments', methods=['GET', 'POST'])
def enrollments():
    conn = get_db_connection()
    if request.method == 'POST':
        data = get_payload()
        student_id = to_int(data.get('student_id'))
        course_id = to_int(data.get('course_id'))
        grade = data.get('grade')

        if not student_id or not course_id:
            conn.close()
            return jsonify({'error': 'student_id and course_id are required'}), 400

        student = conn.execute(
            'SELECT id FROM students WHERE id = ?',
            (student_id,),
        ).fetchone()
        course = conn.execute(
            'SELECT id FROM courses WHERE id = ?',
            (course_id,),
        ).fetchone()

        if not student or not course:
            conn.close()
            return jsonify({'error': 'student_id or course_id does not exist'}), 400

        try:
            cursor = conn.execute(
                'INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)',
                (student_id, course_id, grade),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            conn.close()
            return jsonify({'error': str(exc)}), 400

        enrollment = conn.execute(
            '''
            SELECT
                e.id,
                e.student_id,
                e.course_id,
                e.enrolled_on,
                e.grade,
                s.name AS student_name,
                c.code AS course_code,
                c.title AS course_title
            FROM enrollments e
            JOIN students s ON s.id = e.student_id
            JOIN courses c ON c.id = e.course_id
            WHERE e.id = ?
            ''',
            (cursor.lastrowid,),
        ).fetchone()
        conn.close()
        return jsonify(dict(enrollment)), 201

    enrollments = conn.execute(
        '''
        SELECT
            e.id,
            e.enrolled_on,
            e.grade,
            s.id AS student_id,
            s.name AS student_name,
            s.email AS student_email,
            c.id AS course_id,
            c.code AS course_code,
            c.title AS course_title,
            c.credits AS course_credits
        FROM enrollments e
        JOIN students s ON s.id = e.student_id
        JOIN courses c ON c.id = e.course_id
        ORDER BY e.id
        '''
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in enrollments])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
