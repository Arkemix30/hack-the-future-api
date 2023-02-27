from fastapi import FastAPI
from sqladmin import Admin

from app.students.admin_views import (
    AdmissionAdmin,
    GuardianAdmin,
    StudentAdmin,
)


def init_admin(app: FastAPI, engine):
    admin = Admin(app, engine, title="Admin Panel")
    admin.add_view(StudentAdmin)
    admin.add_view(AdmissionAdmin)
    admin.add_view(GuardianAdmin)
