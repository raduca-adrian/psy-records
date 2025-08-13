"""
User Interface Components

This package contains all PyQt6 dialog and window classes for the application.
"""

from .main_window import MainWindow
from .login_dialog import LoginDialog
from .medical_records_window import MedicalRecordsWindow
from .person_dialog import PersonDialog
from .assessment_dialog import AssessmentDialog
from .consultation_dialog import ConsultationDialog
from .change_password_dialog import ChangePasswordDialog

__all__ = [
    "MainWindow",
    "LoginDialog", 
    "MedicalRecordsWindow",
    "PersonDialog",
    "AssessmentDialog",
    "ConsultationDialog",
    "ChangePasswordDialog",
]
