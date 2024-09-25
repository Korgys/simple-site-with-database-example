from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/students', methods=['GET', 'POST'])
def students():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        conn.execute('INSERT INTO students (name) VALUES (?)', (name,))
        conn.commit()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
