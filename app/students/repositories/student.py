# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
from app.infrastructure import get_db_session
from app.students.entities import Student
from app.utils.errors import DatabaseError, handle_database_error

logger = get_logger(__name__)


class StudentRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    @handle_database_error
    def get(self, id: str) -> Union[Student, DatabaseError]:
        """
        Get an Student by id.

        Parameters
        ----------
        `id` : str
            The id of the student to get

        Returns
        -------
        `Union[Student, DatabaseError]`
            The student if found, otherwise an DatabaseError
        """
        try:
            statement = select(Student).where(Student.id == id)
            return self.session.exec(statement).first()
        except Exception as err:
            logger.error(f"Error getting Student, Error: {err}")
            raise err

    @handle_database_error
    def get_all(self) -> Union[list[Student], DatabaseError]:
        """
        Get all Students.

        Returns
        -------
        `Union[list[Student], DatabaseError]`
            A list of students if found, otherwise an DatabaseError
        """
        statement = select(Student)
        try:
            return self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(f"Error while fetching all Students, error: {err}")
            raise err

    @handle_database_error
    def create(self, student: Student) -> Union[Student, DatabaseError]:
        """
        Create a student

        Parameters
        ----------
        `student` : Student
            The student to create

        Returns
        -------
        `Union[Student, DatabaseError]`
            The created Student if successful, otherwise an DatabaseError
        """

        try:
            self.session.add(student)
            self.session.commit()
            self.session.refresh(student)
            return student
        except Exception as err:
            logger.error(f"Error while creating Student, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def bulk_create(
        self, students: list[Student]
    ) -> Union[bool, DatabaseError]:
        """
        Create multiple students

        Parameters
        ----------
        `students` : list[Student]
            The Students to create

        Returns
        -------
        `Union[bool, DatabaseError]`
            True if successful, otherwise an DatabaseError
        """

        try:
            self.session.add_all(students)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while creating Students, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def update(self, student: Student) -> Union[Student, DatabaseError]:
        try:
            self.session.add(student)
            self.session.commit()
            self.session.refresh(student)
        except Exception as err:
            logger.error(f"Error while updating Student, error: {err}")
            self.session.rollback()
            raise err
        return student

    @handle_database_error
    def delete(self, student: Student) -> Union[bool, DatabaseError]:
        try:
            self.session.delete(student)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while deleting Student, error: {err}")
            self.session.rollback()
            raise err
