# isort: skip_file
import json

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core import get_logger
from app.students.entities import Student
from app.students.schemas.student import (
    StudentCreateSchema,
    StudentUpdateSchema,
)
from app.students.services.student import StudentService
from app.utils.errors import AppError


logger = get_logger(__name__)
student_router = APIRouter()


@student_router.get("/", response_model=list[Student])
async def list_students(
    student_service: StudentService = Depends(),
) -> list[Student]:
    result = student_service.get_all()
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return result


@student_router.get("/{id}", response_model=Student)
async def retrieve_student(
    id: str,
    student_service: StudentService = Depends(),
) -> Student:
    student = student_service.get(id)
    if student:
        return student
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )


@student_router.post("/", response_model=Student)
async def create_event(
    student: StudentCreateSchema,
    student_service: StudentService = Depends(),
) -> Student:
    result = student_service.create(student)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@student_router.post("/bulk_create")
async def bulk_create_students(
    students: list[StudentCreateSchema],
    student_service: StudentService = Depends(),
) -> Response:
    result = student_service.bulk_create(students)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Students created succesfully"}),
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


@student_router.put("/{id}", response_model=Student)
async def update_student(
    id: str,
    student: StudentUpdateSchema,
    student_service: StudentService = Depends(),
) -> Student:
    result = student_service.update(id, student)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@student_router.delete("/{id}")
async def delete_event(
    id: str,
    student_service: StudentService = Depends(),
) -> Student:
    result = student_service.delete(id)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Student deleted succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
