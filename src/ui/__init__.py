"""
User Interface Components

This package contains all PyQt6 dialog and window classes for the application.
"""

from .main_window import MainWindow
from .modern_main_window import ModernMainWindow
from .login_dialog import LoginDialog
from .medical_records_window import MedicalRecordsWindow
from .modern_medical_records_window import ModernMedicalRecordsWindow
from .person_dialog import PersonDialog
from .assessment_dialog import AssessmentDialog
from .consultation_dialog import ConsultationDialog
from .change_password_dialog import ChangePasswordDialog

# Modern UI components
from .modern_qss import ModernQSS, ResponsiveStyleManager, get_style_manager
from .responsive_layout import ResponsiveWidget, FlexibleLayout, ResponsiveBreakpoints

__all__ = [
    "MainWindow",
    "ModernMainWindow",
    "LoginDialog", 
    "MedicalRecordsWindow",
    "ModernMedicalRecordsWindow",
    "PersonDialog",
    "AssessmentDialog",
    "ConsultationDialog",
    "ChangePasswordDialog",
    # Modern UI components
    "ModernQSS",
    "ResponsiveStyleManager", 
    "get_style_manager",
    "ResponsiveWidget",
    "FlexibleLayout",
    "ResponsiveBreakpoints",
]
