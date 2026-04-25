# Simple Site With Database Example

A small Flask app that uses a local SQLite database to store student names.

## What it does

- Serves a basic home page at `/`
- Exposes a `/students` endpoint
- Supports:
  - `GET /students` to list all saved students as JSON
  - `POST /students` to add a new student name

## How it works

- `app.py` runs the Flask app and talks to `database.db`
- `schema.sql` defines the `students` table
- `init_db.py` creates or resets the database from `schema.sql`

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create the database:

   ```bash
   python init_db.py
   ```

3. Start the app:

   ```bash
   python app.py
   ```

4. Open the app in your browser:

   ```text
   http://localhost:5000
   ```

## Example request

```bash
curl -X POST -F "name=Alice" http://localhost:5000/students
```

Then visit:

```text
http://localhost:5000/students
```

to see the stored records.
