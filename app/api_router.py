from fastapi import APIRouter

from app.students.routes import student_module_router

api_router = APIRouter()
api_router.include_router(
    student_module_router, prefix="/students", tags=["students"]
)
