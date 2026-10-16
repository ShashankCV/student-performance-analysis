from datetime import date

from fastapi import APIRouter, HTTPException, Path, Query

from app.database import get_connection, row_to_dict
from app.schemas import StudentRead


router = APIRouter(tags=["students"])


@router.get("/students", response_model=list[StudentRead])
def list_students(
    name: str | None = Query(default=None, min_length=1),
    course: str | None = Query(default=None, min_length=1),
    date_of_birth_after: date | None = None,
    date_of_birth_before: date | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
) -> list[dict]:
    conditions: list[str] = []
    parameters: list[object] = []

    if name:
        conditions.append("name LIKE ? COLLATE NOCASE")
        parameters.append(f"%{name.strip()}%")
    if course:
        conditions.append("course LIKE ? COLLATE NOCASE")
        parameters.append(f"%{course.strip()}%")
    if date_of_birth_after:
        conditions.append("date_of_birth > ?")
        parameters.append(date_of_birth_after.isoformat())
    if date_of_birth_before:
        conditions.append("date_of_birth < ?")
        parameters.append(date_of_birth_before.isoformat())

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    parameters.extend((limit, offset))
    with get_connection() as connection:
        rows = connection.execute(
            f"SELECT * FROM students {where_clause} ORDER BY student_id LIMIT ? OFFSET ?",
            parameters,
        ).fetchall()
    return [row_to_dict(row) for row in rows]


@router.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int = Path(ge=1)) -> dict:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return row_to_dict(row)