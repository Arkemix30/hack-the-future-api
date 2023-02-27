from sqladmin import ModelView

from app.students.entities import Admission, Guardian, Student


class StudentAdmin(ModelView, model=Student):
    column_list = [
        Student.id,
        Student.first_name,
        Student.last_name,
        Student.date_of_birth,
        Student.created_at,
        Student.updated_at,
    ]

    icon = "fa fa-users"


class AdmissionAdmin(ModelView, model=Admission):
    column_list = [
        Admission.id,
        Admission.date,
        Admission.student_id,
        Admission.created_at,
        Admission.updated_at,
    ]

    icon = "fa fa-users"


class GuardianAdmin(ModelView, model=Guardian):
    column_list = [
        Guardian.id,
        Guardian.first_name,
        Guardian.last_name,
        Guardian.cell_phone,
        Guardian.email,
        Guardian.student_id,
        Guardian.created_at,
        Guardian.updated_at,
    ]

    icon = "fa fa-users"
