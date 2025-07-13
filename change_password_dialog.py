from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                            QPushButton, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ChangePasswordDialog(QDialog):
    def __init__(self, db_manager, username):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Change Password")
        self.setFixedSize(350, 200)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Change Password")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        
        # Form layout
        form_layout = QFormLayout()
        
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password.setPlaceholderText("Enter current password")
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setPlaceholderText("Enter new password")
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setPlaceholderText("Confirm new password")
        
        form_layout.addRow("Current Password:", self.current_password)
        form_layout.addRow("New Password:", self.new_password)
        form_layout.addRow("Confirm Password:", self.confirm_password)
        
        # Buttons
        button_layout = QVBoxLayout()
        
        change_button = QPushButton("Change Password")
        change_button.clicked.connect(self.change_password)
        change_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
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
        
        button_layout.addWidget(change_button)
        button_layout.addWidget(cancel_button)
        
        # Add to main layout
        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Connect Enter key
        self.confirm_password.returnPressed.connect(self.change_password)
        
        # Apply stylesheet
        self.setStyleSheet("""
            QDialog {
                background-color: #ecf0f1;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
            }
        """)
    
    def change_password(self):
        current_pass = self.current_password.text().strip()
        new_pass = self.new_password.text().strip()
        confirm_pass = self.confirm_password.text().strip()
        
        # Validate inputs
        if not all([current_pass, new_pass, confirm_pass]):
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "New passwords do not match.")
            return
        
        if len(new_pass) < 6:
            QMessageBox.warning(self, "Error", "New password must be at least 6 characters long.")
            return
        
        if current_pass == new_pass:
            QMessageBox.warning(self, "Error", "New password must be different from current password.")
            return
        
        # Change password
        if self.db_manager.change_password(self.username, current_pass, new_pass):
            QMessageBox.information(self, "Success", "Password changed successfully!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", 
                               "Failed to change password. Please check your current password.")
