from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QTextEdit, QPushButton, QDateEdit,
                            QMessageBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from ..utils.language_manager import get_language_manager, get_text as lang_get_text

class AssessmentDialog(QDialog):
    def __init__(self, person_name, person_id, assessment_data=None, parent=None):
        super().__init__(parent)
        self.person_name = person_name
        self.person_id = person_id
        self.assessment_data = assessment_data
        self.is_edit_mode = assessment_data is not None
        
        self.init_ui()
        
        # If editing, populate fields
        if self.is_edit_mode:
            self.populate_fields()
    
    def init_ui(self):
        self.setWindowTitle(f"{'Edit' if self.is_edit_mode else 'New'} Assessment - {self.person_name}")
        self.setModal(True)
        self.resize(800, 600)
        
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Header
        header_label = QLabel(f"{'Edit' if self.is_edit_mode else 'New'} Psychological Assessment")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(header_label)
        
        patient_label = QLabel(f"Client: {self.person_name}")
        patient_label.setStyleSheet("color: #6c757d; font-weight: 500; margin: 10px 0;")
        scroll_layout.addWidget(patient_label)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Assessment Date
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Assessment Date:", self.date_edit)
        
        # Presenting Problem
        self.chief_complaint_edit = QTextEdit()
        self.chief_complaint_edit.setMaximumHeight(80)
        self.chief_complaint_edit.setPlaceholderText("Primary presenting problem or concern...")
        form_layout.addRow("Presenting Problem:", self.chief_complaint_edit)
        
        # Psychological History
        self.medical_history_edit = QTextEdit()
        self.medical_history_edit.setMaximumHeight(100)
        self.medical_history_edit.setPlaceholderText("Previous therapy, mental health history, family history...")
        form_layout.addRow("Psychological History:", self.medical_history_edit)
        
        # Mental Status Exam
        self.physical_exam_edit = QTextEdit()
        self.physical_exam_edit.setMaximumHeight(120)
        self.physical_exam_edit.setPlaceholderText("Appearance, mood, affect, thought process, cognition, insight...")
        form_layout.addRow("Mental Status Exam:", self.physical_exam_edit)
        
        # Clinical Impressions/Diagnosis
        self.diagnosis_edit = QTextEdit()
        self.diagnosis_edit.setMaximumHeight(80)
        self.diagnosis_edit.setPlaceholderText("DSM-5 diagnoses, clinical impressions...")
        form_layout.addRow("Clinical Impressions:", self.diagnosis_edit)
        
        # Treatment Goals & Plan
        self.treatment_plan_edit = QTextEdit()
        self.treatment_plan_edit.setMaximumHeight(120)
        self.treatment_plan_edit.setPlaceholderText("Treatment goals, therapeutic approach, frequency...")
        form_layout.addRow("Treatment Goals & Plan:", self.treatment_plan_edit)
        
        # Risk Assessment
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setPlaceholderText("Suicide/self-harm risk, safety concerns, additional notes...")
        form_layout.addRow("Risk Assessment & Notes:", self.notes_edit)
        
        scroll_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save Assessment")
        self.save_button.clicked.connect(self.save_assessment)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        scroll_layout.addLayout(button_layout)
        
        # Set up scroll area
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Apply enhanced styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #212529;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-weight: 700;
                color: #000000;
                font-size: 16px;
                margin-bottom: 8px;
                min-height: 32px;
                padding: 8px 0px;
            }
            QLineEdit, QDateEdit {
                padding: 16px 20px;
                border: 3px solid #6c757d;
                border-radius: 8px;
                font-size: 16px;
                background-color: white;
                color: #000000;
                selection-background-color: #0d6efd;
                selection-color: white;
                min-height: 30px;
                max-height: 60px;
                font-weight: 600;
                margin: 6px 0px;
            }
            QTextEdit {
                padding: 16px 20px;
                border: 3px solid #6c757d;
                border-radius: 8px;
                font-size: 16px;
                background-color: white;
                color: #000000;
                selection-background-color: #0d6efd;
                selection-color: white;
                min-height: 120px;
                font-weight: 600;
                margin: 6px 0px;
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.5;
            }
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
                box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.15);
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 16px;
                min-width: 140px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QPushButton[text="Cancel"] {
                background-color: #6c757d;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #5c636a;
            }
            QPushButton[text="Cancel"]:pressed {
                background-color: #565e64;
            }
            QScrollArea {
                border: none;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #6c757d;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #e9ecef;
            }
            QDateEdit::down-arrow {
                image: none;
                border: 2px solid #6c757d;
                width: 3px;
                height: 3px;
            }
        """)
    
    def populate_fields(self):
        """Populate fields when editing an existing assessment."""
        if not self.assessment_data:
            return
        
        # assessment_data is a tuple from database query
        # (id, assessment_date, chief_complaint, medical_history, physical_examination, 
        #  diagnosis, treatment_plan, notes, created_at, updated_at)
        
        assessment_id, assessment_date, chief_complaint, medical_history, physical_examination, diagnosis, treatment_plan, notes, created_at, updated_at = self.assessment_data
        
        # Set date
        if assessment_date:
            date = QDate.fromString(assessment_date, "yyyy-MM-dd")
            self.date_edit.setDate(date)
        
        # Set text fields
        self.chief_complaint_edit.setPlainText(chief_complaint or "")
        self.medical_history_edit.setPlainText(medical_history or "")
        self.physical_exam_edit.setPlainText(physical_examination or "")
        self.diagnosis_edit.setPlainText(diagnosis or "")
        self.treatment_plan_edit.setPlainText(treatment_plan or "")
        self.notes_edit.setPlainText(notes or "")
    
    def save_assessment(self):
        """Save the assessment data."""
        # Get form data
        assessment_date = self.date_edit.date().toString("yyyy-MM-dd")
        chief_complaint = self.chief_complaint_edit.toPlainText().strip()
        medical_history = self.medical_history_edit.toPlainText().strip()
        physical_examination = self.physical_exam_edit.toPlainText().strip()
        diagnosis = self.diagnosis_edit.toPlainText().strip()
        treatment_plan = self.treatment_plan_edit.toPlainText().strip()
        notes = self.notes_edit.toPlainText().strip()
        
        # Validate required fields
        if not chief_complaint and not diagnosis:
            QMessageBox.warning(self, "Validation Error", 
                               "Please provide at least a chief complaint or diagnosis.")
            return
        
        # Store the data for parent to access
        self.result_data = {
            'person_id': self.person_id,
            'assessment_date': assessment_date,
            'chief_complaint': chief_complaint,
            'medical_history': medical_history,
            'physical_examination': physical_examination,
            'diagnosis': diagnosis,
            'treatment_plan': treatment_plan,
            'notes': notes
        }
        
        if self.is_edit_mode:
            self.result_data['assessment_id'] = self.assessment_data[0]
        
        self.accept()
    
    def get_assessment_data(self):
        """Get the assessment data after dialog is accepted."""
        return getattr(self, 'result_data', None)
