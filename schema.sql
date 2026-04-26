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
    ('Adrien Moreau', 'adrien.moreau@exemple.fr'),
    ('Baptiste Laurent', 'baptiste.laurent@exemple.fr'),
    ('Camille Bernard', 'camille.bernard@exemple.fr'),
    ('Damien Petit', 'damien.petit@exemple.fr'),
    ('Estelle Rousseau', 'estelle.rousseau@exemple.fr'),
    ('Florian Fournier', 'florian.fournier@exemple.fr'),
    ('Gaspard Lambert', 'gaspard.lambert@exemple.fr'),
    ('Heloise Laurent', 'heloise.laurent@exemple.fr'),
    ('Julien Renault', 'julien.renault@exemple.fr'),
    ('Lucie Fontaine', 'lucie.fontaine@exemple.fr'),
    ('Malo Chevalier', 'malo.chevalier@exemple.fr'),
    ('Ninon Dubois', 'ninon.dubois@exemple.fr'),
    ('Olivier Girard', 'olivier.girard@exemple.fr'),
    ('Pauline Leroy', 'pauline.leroy@exemple.fr'),
    ('Romain Faure', 'romain.faure@exemple.fr'),
    ('Solene Mercier', 'solene.mercier@exemple.fr'),
    ('Theo Lefevre', 'theo.lefevre@exemple.fr'),
    ('Ugo Blanc', 'ugo.blanc@exemple.fr'),
    ('Victoire Masson', 'victoire.masson@exemple.fr'),
    ('Yann Garnier', 'yann.garnier@exemple.fr');

INSERT INTO courses (code, title, credits) VALUES
    ('FLK101', 'Bases de Flask', 3),
    ('DBS201', 'Conception de bases de données', 4),
    ('API301', 'Développement d''API', 3),
    ('SQL102', 'SQL pratique', 3),
    ('WEB210', 'Développement web', 4),
    ('JIN220', 'Introduction à Jinja', 2),
    ('TST330', 'Tests applicatifs', 3),
    ('DEP410', 'Déploiement d''applications', 4),
    ('SEC120', 'Sécurité des applications', 3),
    ('INT500', 'Projet d''intégration', 5);

INSERT INTO enrollments (student_id, course_id, grade) VALUES
    (1, 1, 'A'),
    (1, 2, 'B+'),
    (1, 4, 'A-'),
    (2, 2, 'A'),
    (2, 3, 'B'),
    (2, 5, 'A-'),
    (3, 1, 'A-'),
    (3, 3, NULL),
    (3, 6, 'B+'),
    (4, 2, 'B'),
    (4, 4, 'A'),
    (4, 7, 'A-'),
    (5, 1, 'A'),
    (5, 5, 'B+'),
    (5, 8, 'A-'),
    (6, 3, 'A'),
    (6, 6, 'B'),
    (6, 9, 'B+'),
    (7, 2, 'A-'),
    (7, 7, 'A'),
    (7, 10, 'B+'),
    (8, 1, 'B+'),
    (8, 4, 'A'),
    (8, 8, 'A-'),
    (9, 3, 'A'),
    (9, 5, 'B'),
    (9, 9, 'A-'),
    (10, 2, 'A'),
    (10, 6, 'A-'),
    (10, 10, 'B+'),
    (11, 1, 'B'),
    (11, 7, 'A-'),
    (11, 8, 'A'),
    (12, 3, 'A-'),
    (12, 4, 'B+'),
    (12, 9, 'B'),
    (13, 2, 'A'),
    (13, 5, 'A-'),
    (13, 10, 'A'),
    (14, 1, 'A-'),
    (14, 6, 'B+'),
    (14, 7, 'A'),
    (15, 3, 'B+'),
    (15, 4, 'A'),
    (15, 8, 'A-'),
    (16, 2, 'A-'),
    (16, 5, 'B'),
    (16, 9, 'A'),
    (17, 1, 'B+'),
    (17, 4, 'A-'),
    (17, 10, 'A'),
    (18, 3, 'A'),
    (18, 6, 'B+'),
    (18, 7, 'A-'),
    (19, 2, 'B'),
    (19, 8, 'A'),
    (19, 9, 'A-'),
    (20, 1, 'A'),
    (20, 5, 'B+'),
    (20, 10, 'A-');
