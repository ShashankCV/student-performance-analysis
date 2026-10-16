import sqlite3

from fastapi import APIRouter, HTTPException, status

from app.database import get_connection, row_to_dict
from app.schemas import StudentCreate, StudentRead


router = APIRouter(tags=["students"])


@router.post("/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate) -> dict:
    fields = student.model_dump(mode="json")
    columns = ", ".join(fields)
    placeholders = ", ".join("?" for _ in fields)

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                f"INSERT INTO students ({columns}) VALUES ({placeholders})",
                list(fields.values()),
            )
            row = connection.execute(
                "SELECT * FROM students WHERE student_id = ?", (cursor.lastrowid,)
            ).fetchone()
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Student could not be created") from exc
    return row_to_dict(row)