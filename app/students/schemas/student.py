from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.students.definitions.enums import GenderType, StudentStatusType


class StudentBaseSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[GenderType]
    date_of_birth: Optional[dt]
    address: Optional[str]
    cell_phone: Optional[str]
    email: Optional[EmailStr]
    status: Optional[StudentStatusType]


class StudentCreateSchema(StudentBaseSchema):
    first_name: str
    last_name: str
    gender: GenderType
    date_of_birth: dt
    status: StudentStatusType


class StudentUpdateSchema(StudentBaseSchema):
    pass
