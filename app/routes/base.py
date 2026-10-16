from fastapi import APIRouter

from app.routes.ai_query import router as ai_query_router
from app.routes.create_student import router as create_student_router
from app.routes.delete_student import router as delete_student_router
from app.routes.get_students import router as get_students_router
from app.routes.update_student import router as update_student_router


router = APIRouter()
router.include_router(create_student_router)
router.include_router(get_students_router)
router.include_router(update_student_router)
router.include_router(delete_student_router)
router.include_router(ai_query_router)