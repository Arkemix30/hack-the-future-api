from enum import Enum
from typing import Optional

from fastapi import status
from pydantic import BaseModel
from sqlalchemy import exc


class ErrorType(Enum):
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    DATASOURCE_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR


class AppError(BaseModel):
    error_type: ErrorType
    message: Optional[str]

    class Config:
        use_enum_values = True


class DatabaseErrorCode(Enum):
    UNIQUE_VIOLATION = "23505"
    FOREIGN_KEY_VIOLATION = "23503"
    CHECK_VIOLATION = "23514"
    NOT_NULL_VIOLATION = "23502"
    INVALID_TRANSACTION_STATE = "25001"
    DATA_ERROR = "22P02"
    OPERATIONAL_ERROR = "55P03"
    PROGRAMMING_ERROR = "42P01"


class DatabaseError(Exception):
    def __init__(self, message, original_exception=None, error_code=None):
        super().__init__(message)
        self.original_exception = original_exception
        self.error_code = error_code


def handle_database_error(func: callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.SQLAlchemyError as err:
            error_code = None
            # sqlstate = None
            # # Get the SQLSTATE error code
            # if isinstance(err, exc.SQLAlchemyError):
            #     sqlstate = str(err.orig.diag.sqlstate)

            # # Check if the error code is in our list of known error codes
            # for code in DatabaseErrorCode:
            #     if code.value == sqlstate:
            #         error_code = code
            #         break

            # Raise our custom error with the relevant information
            raise DatabaseError(str(err), err, error_code)

    return wrapper
