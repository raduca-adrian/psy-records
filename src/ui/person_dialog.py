from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                            QPushButton, QMessageBox, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..utils.language_manager import get_language_manager, get_text as lang_get_text
import re

class PersonDialog(QDialog):
    def __init__(self, db_manager, person_data=None):
        super().__init__()
        self.db_manager = db_manager
        self.person_data = person_data  # For editing existing person
        self.is_edit_mode = person_data is not None
        self.init_ui()
        
        if self.is_edit_mode:
            self.populate_fields()
    
    def init_ui(self):
        title = "Edit Person" if self.is_edit_mode else "Add New Person"
        self.setWindowTitle(title)
        self.setFixedSize(500, 350)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        
        # Form layout
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        self.name_input.setMaxLength(100)
        
        self.cnp_input = QLineEdit()
        self.cnp_input.setPlaceholderText("Enter CNP (13 digits)")
        self.cnp_input.setMaxLength(13)
        
        # Add input validation for CNP (only digits)
        self.cnp_input.textChanged.connect(self.validate_cnp_input)
        
        form_layout.addRow("Full Name:", self.name_input)
        form_layout.addRow("CNP:", self.cnp_input)
        
        # Info label for CNP
        cnp_info = QLabel("CNP must be exactly 13 digits")
        cnp_info.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        form_layout.addRow("", cnp_info)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Update" if self.is_edit_mode else "Add Person")
        save_button.clicked.connect(self.save_person)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        # Add to main layout
        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Connect Enter key
        self.cnp_input.returnPressed.connect(self.save_person)
        
        # Apply enhanced stylesheet for better visibility
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #212529;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
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
            QLineEdit:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
                box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.15);
            }
            QLineEdit::placeholder {
                color: #495057;
                font-style: italic;
                font-weight: 500;
            }
            QLabel {
                font-weight: 700;
                color: #000000;
                font-size: 16px;
                margin-bottom: 8px;
                min-height: 32px;
                padding: 8px 0px;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 16px;
                min-width: 120px;
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
        """)
    
    def validate_cnp_input(self, text):
        """Allow only digits in CNP input"""
        # Remove any non-digit characters
        digits_only = re.sub(r'[^0-9]', '', text)
        if digits_only != text:
            self.cnp_input.setText(digits_only)
    
    def populate_fields(self):
        """Populate fields with existing person data"""
        if self.person_data:
            self.name_input.setText(self.person_data[1])  # name
            self.cnp_input.setText(self.person_data[2])   # cnp
    
    def validate_cnp(self, cnp):
        """Validate Romanian CNP format"""
        if len(cnp) != 13:
            return False, "CNP must be exactly 13 digits"
        
        if not cnp.isdigit():
            return False, "CNP must contain only digits"
        
        # Basic CNP validation (first digit should be 1-8)
        if cnp[0] not in '12345678':
            return False, "Invalid CNP format"
        
        return True, ""
    
    def save_person(self):
        name = self.name_input.text().strip()
        cnp = self.cnp_input.text().strip()
        
        # Validate inputs
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a name.")
            return
        
        if not cnp:
            QMessageBox.warning(self, "Error", "Please enter a CNP.")
            return
        
        # Validate CNP
        is_valid, error_msg = self.validate_cnp(cnp)
        if not is_valid:
            QMessageBox.warning(self, "Error", error_msg)
            return
        
        # Save to database
        if self.is_edit_mode:
            person_id = self.person_data[0]
            if self.db_manager.update_person(person_id, name, cnp):
                QMessageBox.information(self, "Success", "Person updated successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", 
                                   "Failed to update person. CNP might already exist.")
        else:
            if self.db_manager.add_person(name, cnp):
                QMessageBox.information(self, "Success", "Person added successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", 
                                   "Failed to add person. CNP might already exist.")
    
    def get_person_data(self):
        """Return the entered person data"""
        return {
            'name': self.name_input.text().strip(),
            'cnp': self.cnp_input.text().strip()
        }
