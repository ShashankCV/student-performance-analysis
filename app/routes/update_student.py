from fastapi import APIRouter, HTTPException, Path

from app.database import get_connection, row_to_dict
from app.schemas import StudentCreate, StudentRead, StudentUpdate


router = APIRouter(tags=["students"])


@router.patch("/students/{student_id}", response_model=StudentRead)
def update_student(student: StudentUpdate, student_id: int = Path(ge=1)) -> dict:
    changes = student.model_dump(exclude_unset=True, mode="json")
    if not changes:
        raise HTTPException(status_code=422, detail="At least one field must be provided")

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Student not found")

        updated_fields = row_to_dict(existing)
        updated_fields.update(changes)
        updated_fields.pop("student_id")
        if not updated_fields.get("email") and not updated_fields.get("phone"):
            raise HTTPException(
                status_code=422,
                detail="At least one of email or phone is required",
            )
        validated = StudentCreate.model_validate(updated_fields)
        validated_fields = validated.model_dump(mode="json")
        assignments = ", ".join(f"{field} = ?" for field in validated_fields)
        connection.execute(
            f"UPDATE students SET {assignments} WHERE student_id = ?",
            [*validated_fields.values(), student_id],
        )
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
    return row_to_dict(row)