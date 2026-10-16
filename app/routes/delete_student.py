from fastapi import APIRouter, HTTPException, Path, Response, status

from app.database import get_connection


router = APIRouter(tags=["students"])


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int = Path(ge=1)) -> Response:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM students WHERE student_id = ?", (student_id,)
        )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)