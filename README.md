# Simple Site With Database Example

A small Flask app backed by SQLite with a few related tables:

- `students`
- `courses`
- `enrollments`

The database is pre-seeded with sample data so you can inspect joins right away.

## What it does

- Serves a JSON home page at `/`
- Exposes endpoints for students, courses, and enrollments
- Demonstrates one-to-many and many-to-many style relationships through `enrollments`

## Database schema

- `students`
  - `id`, `name`, `email`
- `courses`
  - `id`, `code`, `title`, `credits`
- `enrollments`
  - `id`, `student_id`, `course_id`, `enrolled_on`, `grade`
  - `student_id` and `course_id` are foreign keys
  - `student_id + course_id` is unique so a student cannot be enrolled twice in the same course

## API endpoints

- `GET /`
  - Lists the available endpoints
- `GET /students`
  - Returns all students with a course count
- `POST /students`
  - Creates a student
  - Body fields: `name`, `email`
- `GET /students/<id>`
  - Returns one student and their enrolled courses
- `GET /students/<id>/courses`
  - Returns only the student’s courses
- `GET /courses`
  - Returns all courses with a student count
- `POST /courses`
  - Creates a course
  - Body fields: `code`, `title`, optional `credits`
- `GET /courses/<id>`
  - Returns one course and the students enrolled in it
- `GET /enrollments`
  - Returns all enrollment rows with joined student and course data
- `POST /enrollments`
  - Creates an enrollment
  - Body fields: `student_id`, `course_id`, optional `grade`

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create or reset the database:

   ```bash
   python init_db.py
   ```

3. Start the app:

   ```bash
   python app.py
   ```

4. Open the app:

   ```text
   http://localhost:5000
   ```

## Example requests

List students:

```bash
curl http://localhost:5000/students
```

Create a student:

```bash
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Alice Martin\",\"email\":\"alice.martin@example.com\"}"
```

Create a course:

```bash
curl -X POST http://localhost:5000/courses \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"PYT101\",\"title\":\"Python Fundamentals\",\"credits\":3}"
```

Create an enrollment:

```bash
curl -X POST http://localhost:5000/enrollments \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":1,\"course_id\":3,\"grade\":\"A\"}"
```

## Connecting with DBeaver

This project uses a local SQLite database file: `database.db`.

1. Open DBeaver.
2. Create a new connection.
3. Choose `SQLite`.
4. For the database file, select the full path to this project’s `database.db`.
5. Finish the wizard and open the connection.

If the app is running from this repository, the file is usually:

```text
C:\Sources\simple-site-with-database-example\database.db
```

Notes:

- Stop the Flask app before running `python init_db.py` if DBeaver has the file open and you want to reset it cleanly.
- DBeaver can browse the tables, run SQL queries, and inspect foreign keys directly against the SQLite file.
