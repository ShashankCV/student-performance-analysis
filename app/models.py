CREATE_STUDENTS_TABLE = """
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    course TEXT,
    address TEXT,
    enrollment_date TEXT,
    CHECK (email IS NOT NULL OR phone IS NOT NULL)
)
"""