from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QTextEdit, QPushButton, QDateEdit,
                            QMessageBox, QScrollArea, QWidget, QComboBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from src.utils.language_manager import get_language_manager, get_text as lang_get_text

class ConsultationDialog(QDialog):
    def __init__(self, person_name, person_id, consultation_data=None, parent=None):
        super().__init__(parent)
        self.person_name = person_name
        self.person_id = person_id
        self.consultation_data = consultation_data
        self.is_edit_mode = consultation_data is not None
        
        self.init_ui()
        
        # If editing, populate fields
        if self.is_edit_mode:
            self.populate_fields()
    
    def init_ui(self):
        self.setWindowTitle(f"{'Edit' if self.is_edit_mode else 'New'} Therapy Session - {self.person_name}")
        self.setModal(True)
        self.resize(800, 600)
        
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Header
        header_label = QLabel(f"{'Edit' if self.is_edit_mode else 'New'} Therapy Session")
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
        
        # Session Date
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Session Date:", self.date_edit)
        
        # Session Type
        self.consultation_type_combo = QComboBox()
        self.consultation_type_combo.addItems([
            "Individual Therapy",
            "Initial Intake", 
            "Crisis Intervention",
            "Group Therapy",
            "Family Therapy",
            "Couples Therapy",
            "Assessment Session",
            "Termination Session"
        ])
        form_layout.addRow("Session Type:", self.consultation_type_combo)
        
        # Session Focus/Issues
        self.symptoms_edit = QTextEdit()
        self.symptoms_edit.setMaximumHeight(100)
        self.symptoms_edit.setPlaceholderText("Main issues discussed, presenting concerns...")
        form_layout.addRow("Session Focus:", self.symptoms_edit)
        
        # Clinical Observations
        self.examination_findings_edit = QTextEdit()
        self.examination_findings_edit.setMaximumHeight(120)
        self.examination_findings_edit.setPlaceholderText("Mood, affect, behavior, cognitive functioning, progress...")
        form_layout.addRow("Clinical Observations:", self.examination_findings_edit)
        
        # Interventions Used
        self.recommendations_edit = QTextEdit()
        self.recommendations_edit.setMaximumHeight(100)
        self.recommendations_edit.setPlaceholderText("Therapeutic techniques, interventions, homework assigned...")
        form_layout.addRow("Interventions Used:", self.recommendations_edit)
        
        # Response & Progress
        self.medications_edit = QTextEdit()
        self.medications_edit.setMaximumHeight(100)
        self.medications_edit.setPlaceholderText("Client response, progress toward goals, compliance...")
        form_layout.addRow("Response & Progress:", self.medications_edit)
        
        # Next Session
        self.next_appointment_edit = QDateEdit()
        self.next_appointment_edit.setDate(QDate.currentDate().addDays(7))
        self.next_appointment_edit.setCalendarPopup(True)
        self.next_appointment_edit.setSpecialValueText("Not scheduled")
        self.next_appointment_edit.setMinimumDate(QDate(1900, 1, 1))
        form_layout.addRow("Next Session:", self.next_appointment_edit)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setPlaceholderText("Additional notes and observations...")
        form_layout.addRow("Notes:", self.notes_edit)
        
        scroll_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save Session Notes")
        self.save_button.clicked.connect(self.save_consultation)
        
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
            QComboBox {
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
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
                box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.15);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 32px;
                border-left: 3px solid #6c757d;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: #e9ecef;
            }
            QComboBox::down-arrow {
                image: none;
                border: 3px solid #495057;
                width: 10px;
                height: 10px;
                border-top: none;
                border-right: none;
                transform: rotate(45deg);
                margin-top: -3px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #0d6efd;
                background-color: white;
                color: #212529;
                selection-background-color: #0d6efd;
                selection-color: white;
                font-size: 13px;
                padding: 4px;
                outline: none;
                font-weight: 500;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                color: #000000;
                background-color: white;
                border: none;
                min-height: 20px;
                font-weight: 600;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #0d6efd;
                color: white;
                font-weight: 700;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #cce7ff;
                color: #000000;
                font-weight: 700;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                min-width: 120px;
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
        """)
    
    def populate_fields(self):
        """Populate fields when editing an existing consultation."""
        if not self.consultation_data:
            return
        
        # consultation_data is a tuple from database query
        # (id, consultation_date, consultation_type, symptoms, examination_findings,
        #  recommendations, medications, next_appointment, notes, created_at, updated_at)
        
        consultation_id, consultation_date, consultation_type, symptoms, examination_findings, recommendations, medications, next_appointment, notes, created_at, updated_at = self.consultation_data
        
        # Set date
        if consultation_date:
            date = QDate.fromString(consultation_date, "yyyy-MM-dd")
            self.date_edit.setDate(date)
        
        # Set consultation type
        if consultation_type:
            index = self.consultation_type_combo.findText(consultation_type)
            if index >= 0:
                self.consultation_type_combo.setCurrentIndex(index)
        
        # Set text fields
        self.symptoms_edit.setPlainText(symptoms or "")
        self.examination_findings_edit.setPlainText(examination_findings or "")
        self.recommendations_edit.setPlainText(recommendations or "")
        self.medications_edit.setPlainText(medications or "")
        self.notes_edit.setPlainText(notes or "")
        
        # Set next appointment
        if next_appointment:
            next_date = QDate.fromString(next_appointment, "yyyy-MM-dd")
            self.next_appointment_edit.setDate(next_date)
    
    def save_consultation(self):
        """Save the consultation data."""
        # Get form data
        consultation_date = self.date_edit.date().toString("yyyy-MM-dd")
        consultation_type = self.consultation_type_combo.currentText()
        symptoms = self.symptoms_edit.toPlainText().strip()
        examination_findings = self.examination_findings_edit.toPlainText().strip()
        recommendations = self.recommendations_edit.toPlainText().strip()
        medications = self.medications_edit.toPlainText().strip()
        notes = self.notes_edit.toPlainText().strip()
        
        # Handle next appointment (may be None)
        next_appointment = None
        if self.next_appointment_edit.date() != QDate(1900, 1, 1):
            next_appointment = self.next_appointment_edit.date().toString("yyyy-MM-dd")
        
        # Validate required fields
        if not symptoms and not examination_findings and not recommendations:
            QMessageBox.warning(self, "Validation Error", 
                               "Please provide at least symptoms, examination findings, or recommendations.")
            return
        
        # Store the data for parent to access
        self.result_data = {
            'person_id': self.person_id,
            'consultation_date': consultation_date,
            'consultation_type': consultation_type,
            'symptoms': symptoms,
            'examination_findings': examination_findings,
            'recommendations': recommendations,
            'medications': medications,
            'next_appointment': next_appointment,
            'notes': notes
        }
        
        if self.is_edit_mode:
            self.result_data['consultation_id'] = self.consultation_data[0]
        
        self.accept()
    
    def get_consultation_data(self):
        """Get the consultation data after dialog is accepted."""
        return getattr(self, 'result_data', None)
