from fastapi import APIRouter

from .student import student_router

student_module_router = APIRouter()
student_module_router.include_router(student_router, tags=["students"])
