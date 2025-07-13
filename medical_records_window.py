from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QTabWidget, QMessageBox, QHeaderView, QFileDialog,
                            QFrame, QSplitter, QTextEdit, QScrollArea, QDialog)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon
import os
from database import DatabaseManager
from assessment_dialog import AssessmentDialog
from consultation_dialog import ConsultationDialog
from pdf_generator import generate_medical_report

class MedicalRecordsWindow(QMainWindow):
    def __init__(self, person_data, db_manager, parent=None):
        super().__init__(parent)
        self.person_data = person_data  # (id, name, cnp, created_at, updated_at)
        self.db_manager = db_manager
        self.person_id = person_data[0]
        self.person_name = person_data[1]
        self.person_cnp = person_data[2]
        
        self.init_ui()
        self.load_medical_records()
    
    def init_ui(self):
        self.setWindowTitle(f"Medical Records - {self.person_name}")
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
        title_label = QLabel(f"Medical Records - {self.person_name}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        info_label = QLabel(f"CNP: {self.person_cnp} | Patient ID: {self.person_id}")
        info_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.add_assessment_btn = QPushButton("📋 New Assessment")
        self.add_assessment_btn.clicked.connect(self.add_assessment)
        
        self.add_consultation_btn = QPushButton("🩺 New Consultation")
        self.add_consultation_btn.clicked.connect(self.add_consultation)
        
        self.generate_report_btn = QPushButton("📄 Generate PDF Report")
        self.generate_report_btn.clicked.connect(self.generate_pdf_report)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_medical_records)
        
        button_layout.addWidget(self.add_assessment_btn)
        button_layout.addWidget(self.add_consultation_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.generate_report_btn)
        button_layout.addWidget(self.refresh_btn)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(info_label)
        header_layout.addLayout(button_layout)
        
        main_layout.addWidget(header_frame)
        
        # Create tab widget for assessments and consultations
        self.tab_widget = QTabWidget()
        
        # Assessments tab
        self.assessments_tab = QWidget()
        self.setup_assessments_tab()
        self.tab_widget.addTab(self.assessments_tab, "📋 Assessments")
        
        # Consultations tab
        self.consultations_tab = QWidget()
        self.setup_consultations_tab()
        self.tab_widget.addTab(self.consultations_tab, "🩺 Consultations")
        
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
            "Date", "Chief Complaint", "Diagnosis", "Treatment Plan", "Created", "Actions"
        ])
        
        # Set column widths
        header = self.assessments_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Chief Complaint
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Diagnosis
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Treatment Plan
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Created
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Actions
        
        self.assessments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.assessments_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.assessments_table)
    
    def setup_consultations_tab(self):
        """Set up the consultations tab."""
        layout = QVBoxLayout(self.consultations_tab)
        
        # Consultations table
        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(7)
        self.consultations_table.setHorizontalHeaderLabels([
            "Date", "Type", "Symptoms", "Findings", "Recommendations", "Next Appt", "Actions"
        ])
        
        # Set column widths
        header = self.consultations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Symptoms
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Findings
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Recommendations
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Next Appt
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Actions
        
        self.consultations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.consultations_table.setAlternatingRowColors(True)
        
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
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("✏️ Edit")
            edit_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 60px; 
                    padding: 6px 12px; 
                    font-size: 11px;
                    background-color: #0d6efd;
                    color: white;
                    border-radius: 4px;
                    font-weight: 600;
                    margin: 1px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            edit_btn.clicked.connect(lambda checked, aid=assessment_id, data=assessment: self.edit_assessment(aid, data))
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 60px; 
                    padding: 6px 12px; 
                    font-size: 11px; 
                    background-color: #dc3545;
                    color: white;
                    border-radius: 4px;
                    font-weight: 600;
                    margin: 1px;
                }
                QPushButton:hover {
                    background-color: #bb2d3b;
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
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("✏️ Edit")
            edit_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 60px; 
                    padding: 6px 12px; 
                    font-size: 11px;
                    background-color: #0d6efd;
                    color: white;
                    border-radius: 4px;
                    font-weight: 600;
                    margin: 1px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            edit_btn.clicked.connect(lambda checked, cid=consultation_id, data=consultation: self.edit_consultation(cid, data))
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setStyleSheet("""
                QPushButton { 
                    min-width: 60px; 
                    padding: 6px 12px; 
                    font-size: 11px; 
                    background-color: #dc3545;
                    color: white;
                    border-radius: 4px;
                    font-weight: 600;
                    margin: 1px;
                }
                QPushButton:hover {
                    background-color: #bb2d3b;
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
            # Get complete medical record
            record = self.db_manager.get_person_complete_record(self.person_id)
            
            if not record:
                QMessageBox.warning(self, "No Data", "No medical records found for this patient.")
                return
            
            # Ask user for save location
            filename = f"Medical_Report_{self.person_name.replace(' ', '_')}_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Medical Report", 
                filename,
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Generate the report
            success = generate_medical_report(
                record['person'],
                record['assessments'],
                record['consultations'],
                file_path
            )
            
            if success:
                QMessageBox.information(self, "Success", 
                                      f"Medical report generated successfully!\n\nSaved to: {file_path}")
                
                # Ask if user wants to open the file
                reply = QMessageBox.question(self, "Open Report", 
                                           "Would you like to open the report now?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    os.startfile(file_path)  # Windows
            else:
                QMessageBox.critical(self, "Error", "Failed to generate medical report.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the report:\n{str(e)}")
