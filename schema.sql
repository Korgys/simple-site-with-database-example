PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    credits INTEGER NOT NULL DEFAULT 3
);

CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrolled_on TEXT NOT NULL DEFAULT (date('now')),
    grade TEXT,
    UNIQUE(student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY(course_id) REFERENCES courses(id) ON DELETE CASCADE
);

INSERT INTO students (name, email) VALUES
    ('Alice Martin', 'alice@example.com'),
    ('Bruno Petit', 'bruno@example.com'),
    ('Chloe Bernard', 'chloe@example.com');

INSERT INTO courses (code, title, credits) VALUES
    ('FLK101', 'Flask Basics', 3),
    ('DBS201', 'Database Design', 4),
    ('API301', 'API Development', 3);

INSERT INTO enrollments (student_id, course_id, grade) VALUES
    (1, 1, 'A'),
    (1, 2, 'B'),
    (2, 2, 'A'),
    (2, 3, 'B+'),
    (3, 1, 'A-'),
    (3, 3, NULL);
