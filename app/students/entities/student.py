from datetime import datetime as dt
from typing import Optional

from pydantic import EmailStr, condecimal
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Column, DateTime, Field, Relationship

from app.students.definitions.enums import GenderType, StudentStatusType
from app.students.utils import next_month
from app.utils.entities_utils import BaseSQLModel, model_class_name_to_lower

TABLE_NAME_PREFIX = "student"


class StudentBaseModel(BaseSQLModel):
    @declared_attr
    def __tablename__(cls):
        return f"{TABLE_NAME_PREFIX}_{model_class_name_to_lower(cls.__name__)}"


class Admission(StudentBaseModel, table=True):
    date: Optional[dt] = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, server_default=func.now()
        )
    )
    # The back_populates argument is used to create a bi-directional relationship
    # between the two models, so that we can access the other model from either
    # model. In this case, we can access the Admission from the Student model, and viceversa.
    student_id: Optional[int] = Field(
        default=None, foreign_key=f"{TABLE_NAME_PREFIX}_student.id"
    )
    student: Optional["Student"] = Relationship(back_populates="admissions")


class Student(StudentBaseModel, table=True):
    first_name: str = Field(default=None, max_length=50, nullable=False)
    last_name: str = Field(default=None, max_length=50, nullable=False)
    gender: GenderType = Field(nullable=False)
    date_of_birth: dt = Field(nullable=False)
    address: Optional[str] = Field(default=None, max_length=100, nullable=True)
    cell_phone: Optional[str] = Field(
        default=None, max_length=8, nullable=True
    )
    email: Optional[EmailStr] = Field(default=None, nullable=True)
    status: StudentStatusType = Field(
        default=StudentStatusType.ACTIVE, nullable=False
    )

    admissions: list[Admission] = Relationship(back_populates="student")
    fees: list["StudentFee"] = Relationship(back_populates="student")
    guardians: list["Guardian"] = Relationship(back_populates="student")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".capitalize()

    def __str__(self) -> str:
        return self.get_full_name()


class StudentFee(StudentBaseModel, table=True):
    total_amount: condecimal(max_digits=10, decimal_places=2)
    valid_until: dt = Field(default=next_month(), nullable=False)
    date_submitted: Optional[dt] = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, server_default=func.now()
        )
    )

    student_id: Optional[int] = Field(
        default=None, foreign_key=f"{TABLE_NAME_PREFIX}_student.id"
    )
    student: Optional[Student] = Relationship(back_populates="fees")

    def __str__(self):
        return (
            f"Fee: {self.student.get_full_name() if self.student else 'No student'}"
            f" {self.date_submitted.strftime('%Y-%m-%d')}"
        )


class Guardian(StudentBaseModel, table=True):
    first_name: str = Field(default=None, max_length=50, nullable=False)
    last_name: str = Field(default=None, max_length=50, nullable=False)
    cell_phone: Optional[str] = Field(
        default=None, max_length=8, nullable=True
    )
    email: Optional[EmailStr] = Field(default=None, nullable=True)
    address: Optional[str] = Field(default=None, max_length=100, nullable=True)
    profession: Optional[str] = Field(
        default=None, max_length=50, nullable=True
    )

    student_id: Optional[int] = Field(
        default=None, foreign_key=f"{TABLE_NAME_PREFIX}_student.id"
    )
    student: Optional[Student] = Relationship(back_populates="guardians")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".capitalize()

    def __str__(self) -> str:
        return self.get_full_name()
