# isort:skip_file
from typing import Union

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core import get_logger
from app.students.entities import Student
from app.students.repositories import StudentRepository
from app.students.schemas import StudentCreateSchema, StudentUpdateSchema
from app.utils.errors import AppError, DatabaseError, ErrorType

logger = get_logger(__name__)


class StudentService:
    def __init__(self, student_repository: StudentRepository = Depends()):
        self.student_repository = student_repository

    def get(self, id: int) -> Union[Student, AppError]:
        event = self.student_repository.get(id)
        if not event:
            logger.error(f"Student not found with id: {id}")
            return None
        return event

    def get_all(self) -> Union[list[Student], AppError]:
        try:
            return self.student_repository.get_all()
        except DatabaseError as err:
            logger.error(f"Error while fetching all Students, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="DB Error while fetching all Students",
            )

    def create(self, student: StudentCreateSchema) -> Union[Student, AppError]:
        student = student(**student.dict())
        try:
            return self.student_repository.create(student)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Student, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating Student",
            )

    def bulk_create(self, students: list[StudentCreateSchema]) -> bool:
        students = [Student(**event.dict()) for event in students]
        try:
            return self.student_repository.bulk_create(students)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Events, error: {err}")
            return False

    def update(self, id: int, student: StudentUpdateSchema) -> Student:
        try:
            student_in_db = self.student_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Student, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Student",
            )

        if not student_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Student not found"
            )

        obj_data = jsonable_encoder(student_in_db)
        if isinstance(student, dict):
            update_data = student
        else:
            update_data = student.dict(exclude_unset=True)

        # This is an iterator over the fields of the model to be updated
        for field in obj_data:
            if field in update_data:
                setattr(student_in_db, field, update_data[field])
        try:
            return self.student_repository.update(student_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while updating Student, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while updating Student",
            )

    def delete(self, id: str) -> Student:
        try:
            student_in_db = self.student_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Student, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Student",
            )

        if isinstance(student_in_db, AppError):
            return student_in_db

        if not student_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Student not found"
            )

        try:
            return self.student_repository.delete(student_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while deleting Student, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while deleting Student",
            )
