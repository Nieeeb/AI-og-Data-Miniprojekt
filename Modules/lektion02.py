import sqlite3
from sqlite3 import Error

# Funktioner der forbinder til en eksisterende database
# Hvis der ikke er en database i path, oprettes der en ny
# Ikke skabt af mig
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Funktioner der gen udføre tilføjelser til databaser
# Ikke skabt af mig
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Funktion der kan læse fra en database
# Ikke skabt af mig
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Oprettelse af Database
connection = create_connection("Data\school.db")

# SQL for students tabel
create_students_table = """
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    major TEXT
);
"""
# Tilføjer students tabel
execute_query(connection, create_students_table)

# SQL for courses tabel
create_courses_table = """
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    instructor_name TEXT
);
"""
# Tilføjer courses tabel
execute_query(connection, create_courses_table)

# SQL til enrollments table
create_enrollments_table = """
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL
);
"""
# Tkføjer enrollments tabel
execute_query(connection, create_enrollments_table)

# SQL til at tiføje studenter
add_students = """
INSERT INTO
    students (student_name, major)
VALUES
    ('Elizabeth', 'Science'),
    ('Oliver', 'Science'),
    ('Andreas', 'Math'),
    ('Mads', 'English'),
    ('William', 'Math');
"""
# Tilføjer studenter
execute_query(connection, add_students)

#SQL til at tilføje courses
add_courses = """
INSERT INTO
    courses (course_name, instructor_name)
VALUES
    ('English', 'Gigachad'),
    ('Math', 'Lars'),
    ('Science', 'Timothy'),
    ('Bikes', 'Bobby'),
    ('AI', 'Kevin');
"""
# Tiføjer courses
execute_query(connection, add_courses)

select_matchin_course_names = "SELECT c.course_id, s.student_id FROM courses AS c, students AS s WHERE c.course_name = s.major" 
matching_majors = execute_read_query(connection, select_matchin_course_names)
# print(matching_majors)

# SQL til at tilføje studenter til enrolments efter deres major
add_enrollments = """
INSERT INTO
    enrollments (course_id, student_id)

    SELECT c.course_id, s.student_id
    FROM courses AS c, students AS s
    WHERE c.course_name = s.major
"""
# Tilføjer students efter major
execute_query(connection, add_enrollments)

# Søger efter matchende student id i enrollments og finder deres navn i students databasen
elizabeth_courses = """
SELECT s.student_name, s.major FROM students AS s, enrollments AS e WHERE e.student_id = s.student_id AND s.student_id = 1
"""
matches = execute_read_query(connection, elizabeth_courses)
print(matches)

# Finder alle studenter der er i english kursus og finder deres navn ud fra student id i student tabel
find_all_math_students = """
SELECT s.student_name
FROM students AS s, enrollments AS e, courses AS c
WHERE c.course_name = 'Math' AND e.course_id = c.course_id AND s.student_id = e.student_id
"""
math_students = execute_read_query(connection, find_all_math_students)
print(math_students)

