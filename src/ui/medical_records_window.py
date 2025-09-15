from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QTabWidget, QMessageBox, QHeaderView, QFileDialog,
                            QFrame, QSplitter, QTextEdit, QScrollArea, QDialog)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon
import os
from ..core.database import DatabaseManager
from .assessment_dialog import AssessmentDialog
from .consultation_dialog import ConsultationDialog
from ..utils.pdf_generator import generate_psychological_report
from ..utils.language_manager import get_language_manager, get_text as lang_get_text
from ..utils.theme_manager import get_theme_manager, ThemeMode

class MedicalRecordsWindow(QMainWindow):
    def __init__(self, person_data, db_manager, parent=None):
        super().__init__(parent)
        self.person_data = person_data  # (id, name, cnp, created_at, updated_at)
        self.db_manager = db_manager
        self.person_id = person_data[0]
        self.person_name = person_data[1]
        self.person_cnp = person_data[2]
        
        # Initialize language manager
        self.language_manager = get_language_manager()
        # Register for language change notifications
        self.language_manager.register_language_change_callback(self.on_language_updated)
        
        # Initialize theme manager
        self.theme_manager = get_theme_manager()
        # Register for theme change notifications  
        self.theme_manager.register_theme_change_callback(self.on_theme_updated)
        
        self.init_ui()
        self.load_medical_records()
        # Apply initial language and theme settings
        self.update_ui_texts()
        self.apply_styling()
    
    def init_ui(self):
        self.setWindowTitle(f"Psychological Records - {self.person_name}")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header section
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_layout = QVBoxLayout(header_frame)
        
        # Patient info header
        self.title_label = QLabel(f"Psychological Records - {self.person_name}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        
        self.info_label = QLabel(f"CNP: {self.person_cnp} | Client ID: {self.person_id}")
        self.info_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.add_assessment_btn = QPushButton(f"📋 {self.get_text('psychological_records.new_assessment')}")
        self.add_assessment_btn.clicked.connect(self.add_assessment)
        
        self.add_consultation_btn = QPushButton(f"💬 {self.get_text('psychological_records.new_session')}")
        self.add_consultation_btn.clicked.connect(self.add_consultation)
        
        self.generate_report_btn = QPushButton(f"📄 {self.get_text('psychological_records.generate_report')}")
        self.generate_report_btn.clicked.connect(self.generate_pdf_report)
        
        self.refresh_btn = QPushButton(f"🔄 {self.get_text('main_window.refresh')}")
        self.refresh_btn.clicked.connect(self.load_medical_records)
        
        # Theme toggle button
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setFixedSize(36, 36)
        self.theme_toggle_btn.setObjectName("theme_toggle_btn")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        
        button_layout.addWidget(self.add_assessment_btn)
        button_layout.addWidget(self.add_consultation_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.generate_report_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.theme_toggle_btn)
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.info_label)
        header_layout.addLayout(button_layout)
        
        main_layout.addWidget(header_frame)
        
        # Create tab widget for assessments and consultations
        self.tab_widget = QTabWidget()
        
        # Assessments tab
        self.assessments_tab = QWidget()
        self.setup_assessments_tab()
        self.tab_widget.addTab(self.assessments_tab, f"📋 {self.get_text('psychological_records.assessments_tab')}")
        
        # Consultations tab
        self.consultations_tab = QWidget()
        self.setup_consultations_tab()
        self.tab_widget.addTab(self.consultations_tab, f"💬 {self.get_text('psychological_records.sessions_tab')}")
        
        main_layout.addWidget(self.tab_widget)
        
        # Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                color: #212529;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            QLabel {
                color: #212529;
                font-weight: 500;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 140px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #0a58ca;
                transform: translateY(0px);
            }
            QPushButton[text*="Assessment"] {
                background-color: #198754;
            }
            QPushButton[text*="Assessment"]:hover {
                background-color: #157347;
            }
            QPushButton[text*="Consultation"] {
                background-color: #6f42c1;
            }
            QPushButton[text*="Consultation"]:hover {
                background-color: #5a359a;
            }
            QPushButton[text*="PDF"] {
                background-color: #fd7e14;
            }
            QPushButton[text*="PDF"]:hover {
                background-color: #e8650e;
            }
            QPushButton[text*="Refresh"] {
                background-color: #6c757d;
            }
            QPushButton[text*="Refresh"]:hover {
                background-color: #5c636a;
            }
            QTabWidget::pane {
                border: 2px solid #dee2e6;
                background-color: white;
                border-radius: 8px;
                padding: 5px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                color: #495057;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #212529;
                border-bottom: 2px solid white;
                margin-bottom: -2px;
            }
            QTabBar::tab:hover {
                background-color: #f8f9fa;
                color: #0d6efd;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                border: 2px solid #0d6efd;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                color: #495057;
                padding: 15px 10px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: 700;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QHeaderView::section:hover {
                background-color: #dee2e6;
                color: #212529;
            }
        """)
    
    def setup_assessments_tab(self):
        """Set up the assessments tab."""
        layout = QVBoxLayout(self.assessments_tab)
        
        # Assessments table
        self.assessments_table = QTableWidget()
        self.assessments_table.setColumnCount(6)
        self.assessments_table.setHorizontalHeaderLabels([
            self.get_text("psychological_records.date"), 
            self.get_text("psychological_records.presenting_problem"), 
            self.get_text("assessment.clinical_impressions"), 
            self.get_text("assessment.treatment_goals"), 
            self.get_text("main_window.created"), 
            self.get_text("psychological_records.actions")
        ])
        
        # Set column widths
        header = self.assessments_table.horizontalHeader()
        header.setVisible(True)  # Ensure headers are visible
        header.setMinimumHeight(40)  # Set minimum height for visibility
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Chief Complaint
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Diagnosis
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Treatment Plan
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Created
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Actions
        header.resizeSection(5, 180)  # Set fixed width for Actions column
        
        self.assessments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.assessments_table.setAlternatingRowColors(True)
        self.assessments_table.verticalHeader().setDefaultSectionSize(50)  # Set row height for buttons
        self.assessments_table.verticalHeader().setVisible(False)  # Hide row numbers
        
        layout.addWidget(self.assessments_table)
    
    def setup_consultations_tab(self):
        """Set up the consultations tab."""
        layout = QVBoxLayout(self.consultations_tab)
        
        # Consultations table
        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(7)
        self.consultations_table.setHorizontalHeaderLabels([
            self.get_text("psychological_records.date"), 
            self.get_text("psychological_records.session_type"), 
            self.get_text("psychological_records.session_focus"), 
            self.get_text("session.clinical_observations"), 
            self.get_text("psychological_records.interventions"), 
            self.get_text("session.next_session"), 
            self.get_text("psychological_records.actions")
        ])
        
        # Set column widths
        header = self.consultations_table.horizontalHeader()
        header.setVisible(True)  # Ensure headers are visible
        header.setMinimumHeight(40)  # Set minimum height for visibility
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Symptoms
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Findings
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Recommendations
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Next Appt
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Actions
        header.resizeSection(6, 180)  # Set fixed width for Actions column
        
        self.consultations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.consultations_table.setAlternatingRowColors(True)
        self.consultations_table.verticalHeader().setDefaultSectionSize(50)  # Set row height for buttons
        self.consultations_table.verticalHeader().setVisible(False)  # Hide row numbers
        
        layout.addWidget(self.consultations_table)
    
    def load_medical_records(self):
        """Load assessments and consultations from database."""
        self.load_assessments()
        self.load_consultations()
    
    def load_assessments(self):
        """Load assessments into the table."""
        assessments = self.db_manager.get_assessments_for_person(self.person_id)
        
        self.assessments_table.setRowCount(len(assessments))
        
        for row, assessment in enumerate(assessments):
            assessment_id, assessment_date, chief_complaint, medical_history, physical_examination, diagnosis, treatment_plan, notes, created_at, updated_at = assessment
            
            # Date
            self.assessments_table.setItem(row, 0, QTableWidgetItem(assessment_date or ""))
            
            # Chief Complaint (truncated)
            chief_complaint_text = (chief_complaint[:50] + "...") if chief_complaint and len(chief_complaint) > 50 else (chief_complaint or "")
            self.assessments_table.setItem(row, 1, QTableWidgetItem(chief_complaint_text))
            
            # Diagnosis (truncated)
            diagnosis_text = (diagnosis[:50] + "...") if diagnosis and len(diagnosis) > 50 else (diagnosis or "")
            self.assessments_table.setItem(row, 2, QTableWidgetItem(diagnosis_text))
            
            # Treatment Plan (truncated)
            treatment_text = (treatment_plan[:50] + "...") if treatment_plan and len(treatment_plan) > 50 else (treatment_plan or "")
            self.assessments_table.setItem(row, 3, QTableWidgetItem(treatment_text))
            
            # Created date
            created_date = created_at.split(' ')[0] if created_at else ""
            self.assessments_table.setItem(row, 4, QTableWidgetItem(created_date))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(8, 4, 8, 4)
            actions_layout.setSpacing(6)
            
            edit_btn = QPushButton(f"✏️ {self.get_text('common.edit')}")
            edit_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 70px; 
                    max-width: 80px;
                    padding: 8px 12px; 
                    font-size: 12px;
                    background-color: #0d6efd !important;
                    color: white !important;
                    border: 2px solid #0d6efd !important;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7 !important;
                    border-color: #0b5ed7 !important;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #0a58ca !important;
                    border-color: #0a58ca !important;
                }
            """)
            edit_btn.clicked.connect(lambda checked, aid=assessment_id, data=assessment: self.edit_assessment(aid, data))
            
            delete_btn = QPushButton(f"🗑️ {self.get_text('common.delete')}")
            delete_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 70px; 
                    max-width: 80px;
                    padding: 8px 12px; 
                    font-size: 12px; 
                    background-color: #dc3545 !important;
                    color: white !important;
                    border: 2px solid #dc3545 !important;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #bb2d3b !important;
                    border-color: #bb2d3b !important;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #b02a37 !important;
                    border-color: #b02a37 !important;
                }
            """)
            delete_btn.clicked.connect(lambda checked, aid=assessment_id: self.delete_assessment(aid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            self.assessments_table.setCellWidget(row, 5, actions_widget)
    
    def load_consultations(self):
        """Load consultations into the table."""
        consultations = self.db_manager.get_consultations_for_person(self.person_id)
        
        self.consultations_table.setRowCount(len(consultations))
        
        for row, consultation in enumerate(consultations):
            consultation_id, consultation_date, consultation_type, symptoms, examination_findings, recommendations, medications, next_appointment, notes, created_at, updated_at = consultation
            
            # Date
            self.consultations_table.setItem(row, 0, QTableWidgetItem(consultation_date or ""))
            
            # Type
            self.consultations_table.setItem(row, 1, QTableWidgetItem(consultation_type or ""))
            
            # Symptoms (truncated)
            symptoms_text = (symptoms[:40] + "...") if symptoms and len(symptoms) > 40 else (symptoms or "")
            self.consultations_table.setItem(row, 2, QTableWidgetItem(symptoms_text))
            
            # Findings (truncated)
            findings_text = (examination_findings[:40] + "...") if examination_findings and len(examination_findings) > 40 else (examination_findings or "")
            self.consultations_table.setItem(row, 3, QTableWidgetItem(findings_text))
            
            # Recommendations (truncated)
            recommendations_text = (recommendations[:40] + "...") if recommendations and len(recommendations) > 40 else (recommendations or "")
            self.consultations_table.setItem(row, 4, QTableWidgetItem(recommendations_text))
            
            # Next Appointment
            self.consultations_table.setItem(row, 5, QTableWidgetItem(next_appointment or "Not scheduled"))
            
            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(8, 4, 8, 4)
            actions_layout.setSpacing(6)
            
            edit_btn = QPushButton(f"✏️ {self.get_text('common.edit')}")
            edit_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 70px; 
                    max-width: 80px;
                    padding: 8px 12px; 
                    font-size: 12px;
                    background-color: #0d6efd !important;
                    color: white !important;
                    border: 2px solid #0d6efd !important;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7 !important;
                    border-color: #0b5ed7 !important;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #0a58ca !important;
                    border-color: #0a58ca !important;
                }
            """)
            edit_btn.clicked.connect(lambda checked, cid=consultation_id, data=consultation: self.edit_consultation(cid, data))
            
            delete_btn = QPushButton(f"🗑️ {self.get_text('common.delete')}")
            delete_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 70px; 
                    max-width: 80px;
                    padding: 8px 12px; 
                    font-size: 12px; 
                    background-color: #dc3545 !important;
                    color: white !important;
                    border: 2px solid #dc3545 !important;
                    border-radius: 6px;
                    font-weight: 600;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #bb2d3b !important;
                    border-color: #bb2d3b !important;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #b02a37 !important;
                    border-color: #b02a37 !important;
                }
            """)
            delete_btn.clicked.connect(lambda checked, cid=consultation_id: self.delete_consultation(cid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            self.consultations_table.setCellWidget(row, 6, actions_widget)
    
    def add_assessment(self):
        """Add a new assessment."""
        dialog = AssessmentDialog(self.person_name, self.person_id, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_assessment_data()
            if data:
                success = self.db_manager.add_assessment(
                    data['person_id'],
                    data['assessment_date'],
                    data['chief_complaint'],
                    data['medical_history'],
                    data['physical_examination'],
                    data['diagnosis'],
                    data['treatment_plan'],
                    data['notes']
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Assessment added successfully!")
                    self.load_assessments()
                else:
                    QMessageBox.critical(self, "Error", "Failed to add assessment.")
    
    def edit_assessment(self, assessment_id, assessment_data):
        """Edit an existing assessment."""
        dialog = AssessmentDialog(self.person_name, self.person_id, assessment_data, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_assessment_data()
            if data:
                success = self.db_manager.update_assessment(
                    assessment_id,
                    data['assessment_date'],
                    data['chief_complaint'],
                    data['medical_history'],
                    data['physical_examination'],
                    data['diagnosis'],
                    data['treatment_plan'],
                    data['notes']
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Assessment updated successfully!")
                    self.load_assessments()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update assessment.")
    
    def delete_assessment(self, assessment_id):
        """Delete an assessment."""
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this assessment?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db_manager.delete_assessment(assessment_id):
                QMessageBox.information(self, "Success", "Assessment deleted successfully!")
                self.load_assessments()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete assessment.")
    
    def add_consultation(self):
        """Add a new consultation."""
        dialog = ConsultationDialog(self.person_name, self.person_id, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_consultation_data()
            if data:
                success = self.db_manager.add_consultation(
                    data['person_id'],
                    data['consultation_date'],
                    data['consultation_type'],
                    data['symptoms'],
                    data['examination_findings'],
                    data['recommendations'],
                    data['medications'],
                    data['next_appointment'],
                    data['notes']
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Consultation added successfully!")
                    self.load_consultations()
                else:
                    QMessageBox.critical(self, "Error", "Failed to add consultation.")
    
    def edit_consultation(self, consultation_id, consultation_data):
        """Edit an existing consultation."""
        dialog = ConsultationDialog(self.person_name, self.person_id, consultation_data, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_consultation_data()
            if data:
                success = self.db_manager.update_consultation(
                    consultation_id,
                    data['consultation_date'],
                    data['consultation_type'],
                    data['symptoms'],
                    data['examination_findings'],
                    data['recommendations'],
                    data['medications'],
                    data['next_appointment'],
                    data['notes']
                )
                
                if success:
                    QMessageBox.information(self, "Success", "Consultation updated successfully!")
                    self.load_consultations()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update consultation.")
    
    def delete_consultation(self, consultation_id):
        """Delete a consultation."""
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this consultation?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db_manager.delete_consultation(consultation_id):
                QMessageBox.information(self, "Success", "Consultation deleted successfully!")
                self.load_consultations()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete consultation.")
    
    def generate_pdf_report(self):
        """Generate a PDF medical report."""
        try:
            # Get complete psychological record
            record = self.db_manager.get_person_complete_record(self.person_id)
            
            if not record:
                QMessageBox.warning(self, "No Data", "No psychological records found for this client.")
                return
            
            # Ask user for save location
            filename = f"Psychological_Report_{self.person_name.replace(' ', '_')}_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Psychological Report", 
                filename,
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Generate the report
            success = generate_psychological_report(
                record['person'],
                record['assessments'],
                record['consultations'],
                file_path
            )
            
            if success:
                QMessageBox.information(self, "Success", 
                                      f"Psychological report generated successfully!\n\nSaved to: {file_path}")
                
                # Ask if user wants to open the file
                reply = QMessageBox.question(self, "Open Report", 
                                           "Would you like to open the report now?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    os.startfile(file_path)  # Windows
            else:
                QMessageBox.critical(self, "Error", "Failed to generate psychological report.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the report:\n{str(e)}")
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)
    
    def on_language_updated(self, locale: str):
        """Called when language is changed from anywhere in the application."""
        self.update_ui_texts()
        self.load_medical_records()  # Refresh tables to update headers
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        # Update window title
        self.setWindowTitle(f"{self.get_text('psychological_records.title')} - {self.person_name}")
        
        # Update main title and info labels
        try:
            self.title_label.setText(f"{self.get_text('psychological_records.title')} - {self.person_name}")
            self.info_label.setText(f"CNP: {self.person_cnp} | {self.get_text('psychological_records.client_id')}: {self.person_id}")
        except (AttributeError, RuntimeError):
            pass
        
        # Update buttons
        try:
            self.add_assessment_btn.setText(f"📋 {self.get_text('psychological_records.new_assessment')}")
            self.add_consultation_btn.setText(f"💬 {self.get_text('psychological_records.new_session')}")
            self.generate_report_btn.setText(f"📄 {self.get_text('psychological_records.generate_report')}")
            self.refresh_btn.setText(f"🔄 {self.get_text('main_window.refresh')}")
            # Update theme toggle button tooltip
            current_theme = self.theme_manager.get_current_theme()
            self.theme_toggle_btn.setToolTip(self.get_text('common.theme_toggle_tooltip'))
        except (AttributeError, RuntimeError):
            pass
        
        # Update tab titles
        try:
            self.tab_widget.setTabText(0, f"📋 {self.get_text('psychological_records.assessments_tab')}")
            self.tab_widget.setTabText(1, f"💬 {self.get_text('psychological_records.sessions_tab')}")
        except (AttributeError, RuntimeError):
            pass
        
        # Update table headers
        try:
            self.assessments_table.setHorizontalHeaderLabels([
                self.get_text("psychological_records.date"), 
                self.get_text("psychological_records.presenting_problem"), 
                self.get_text("assessment.clinical_impressions"), 
                self.get_text("assessment.treatment_goals"), 
                self.get_text("main_window.created"), 
                self.get_text("psychological_records.actions")
            ])
        except (AttributeError, RuntimeError):
            pass
        
        try:
            self.consultations_table.setHorizontalHeaderLabels([
                self.get_text("psychological_records.date"), 
                self.get_text("psychological_records.session_type"), 
                self.get_text("psychological_records.session_focus"), 
                self.get_text("session.clinical_observations"), 
                self.get_text("psychological_records.interventions"), 
                self.get_text("session.next_session"), 
                self.get_text("psychological_records.actions")
            ])
        except (AttributeError, RuntimeError):
            pass
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        current_theme = self.theme_manager.get_current_theme()
        new_theme = ThemeMode.DARK if current_theme == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.theme_manager.change_theme(new_theme)
    
    def on_theme_updated(self, theme_mode: ThemeMode):
        """Called when theme is changed from anywhere in the application."""
        self.apply_styling()
        
    def apply_styling(self):
        """Apply theme-aware styling to the window."""
        from .styles import colors
        
        current_theme = self.theme_manager.get_current_theme()
        
        # Update theme toggle button icon and tooltip
        if current_theme == ThemeMode.DARK:
            self.theme_toggle_btn.setText("☀️")
            self.theme_toggle_btn.setToolTip(self.get_text('common.theme_toggle_tooltip'))
        else:
            self.theme_toggle_btn.setText("🌙")
            self.theme_toggle_btn.setToolTip(self.get_text('common.theme_toggle_tooltip'))
            
        # Apply theme-aware styling to the main window
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {colors.background};
                color: {colors.text};
            }}
            QFrame {{
                background-color: {colors.card_background};
                border: 1px solid {colors.border};
                border-radius: 8px;
                padding: 10px;
            }}
            QLabel {{
                color: {colors.text};
                background-color: transparent;
            }}
            QPushButton {{
                background-color: {colors.primary};
                color: {colors.primary_text};
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {colors.primary_hover};
            }}
            QPushButton:pressed {{
                background-color: {colors.primary_pressed};
            }}
            QPushButton#theme_toggle_btn {{
                background-color: {colors.surface};
                color: {colors.text};
                border: 2px solid {colors.border};
                border-radius: 18px;
                padding: 6px;
                font-size: 16px;
                min-width: 32px;
                min-height: 32px;
            }}
            QPushButton#theme_toggle_btn:hover {{
                background-color: {colors.surface_variant};
                border-color: {colors.primary};
            }}
            QTabWidget::pane {{
                border: 1px solid {colors.border};
                background-color: {colors.surface};
            }}
            QTabBar::tab {{
                background-color: {colors.surface};
                color: {colors.text};
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border: 1px solid {colors.border};
            }}
            QTabBar::tab:selected {{
                background-color: {colors.primary};
                color: {colors.primary_text};
            }}
            QTableWidget {{
                background-color: {colors.surface};
                color: {colors.text};
                gridline-color: {colors.border};
                border: 1px solid {colors.border};
            }}
            QTableWidget QWidget {{
                background-color: transparent;
            }}
            QTableWidget QWidget QPushButton {{
                background-color: #0d6efd;
                color: white;
                border: 2px solid #0d6efd;
                border-radius: 6px;
                font-weight: 600;
                min-width: 70px;
                padding: 8px 12px;
            }}
            QTableWidget QWidget QPushButton:hover {{
                background-color: #0b5ed7;
                border-color: #0b5ed7;
            }}
            QHeaderView::section {{
                background-color: {colors.primary};
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid {colors.border};
                font-weight: 700;
                font-size: 14px;
                min-height: 40px;
                text-align: center;
            }}
            QHeaderView::section:hover {{
                background-color: {colors.primary_hover};
            }}
            QHeaderView::section:pressed {{
                background-color: {colors.primary_pressed};
            }}
            QScrollArea {{
                background-color: {colors.surface};
                border: 1px solid {colors.border};
            }}
        """)
    
    def closeEvent(self, event):
        """Clean up when window is closed."""
        # Unregister language change callback
        if hasattr(self, 'language_manager'):
            self.language_manager.unregister_language_change_callback(self.on_language_updated)
        # Unregister theme change callback  
        if hasattr(self, 'theme_manager'):
            self.theme_manager.unregister_theme_change_callback(self.on_theme_updated)
        super().closeEvent(event)
