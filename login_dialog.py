import sys
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QTabWidget,
                            QWidget, QFormLayout, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from database import DatabaseManager
import os

class LoginDialog(QDialog):
    login_successful = pyqtSignal(str)  # Signal emitted when login is successful
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Secure Application - Login")
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Secure Database Application")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Login tab
        login_tab = QWidget()
        login_layout = QFormLayout()
        
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.db_password_input.setPlaceholderText("Enter database password")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        
        login_layout.addRow("Database Password:", self.db_password_input)
        login_layout.addRow("Username:", self.username_input)
        login_layout.addRow("Password:", self.password_input)
        
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        login_button.setStyleSheet("""
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
        
        login_layout.addRow("", login_button)
        login_tab.setLayout(login_layout)
        
        # Setup tab
        setup_tab = QWidget()
        setup_layout = QFormLayout()
        
        self.setup_db_password = QLineEdit()
        self.setup_db_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.setup_db_password.setPlaceholderText("Create database password")
        
        self.setup_db_password_confirm = QLineEdit()
        self.setup_db_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.setup_db_password_confirm.setPlaceholderText("Confirm database password")
        
        self.setup_username = QLineEdit()
        self.setup_username.setPlaceholderText("Create username")
        
        self.setup_password = QLineEdit()
        self.setup_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.setup_password.setPlaceholderText("Create user password")
        
        self.setup_password_confirm = QLineEdit()
        self.setup_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.setup_password_confirm.setPlaceholderText("Confirm user password")
        
        setup_layout.addRow("Database Password:", self.setup_db_password)
        setup_layout.addRow("Confirm DB Password:", self.setup_db_password_confirm)
        setup_layout.addRow("Username:", self.setup_username)
        setup_layout.addRow("User Password:", self.setup_password)
        setup_layout.addRow("Confirm Password:", self.setup_password_confirm)
        
        setup_button = QPushButton("Create Database & User")
        setup_button.clicked.connect(self.setup_database)
        setup_button.setStyleSheet("""
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
        
        setup_layout.addRow("", setup_button)
        setup_tab.setLayout(setup_layout)
        
        # Add tabs
        tab_widget.addTab(login_tab, "Login")
        
        # Only show setup tab if database doesn't exist
        if not os.path.exists("secure_app.db.enc"):
            tab_widget.addTab(setup_tab, "Initial Setup")
            tab_widget.setCurrentIndex(1)  # Start with setup tab
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(tab_widget)
        
        self.setLayout(main_layout)
        
        # Connect Enter key to login
        self.password_input.returnPressed.connect(self.login)
        self.db_password_input.returnPressed.connect(self.login)
        
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
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3498db;
            }
        """)
    
    def login(self):
        db_password = self.db_password_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not all([db_password, username, password]):
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        # Try to connect to database
        if not self.db_manager.connect(db_password):
            QMessageBox.critical(self, "Error", "Invalid database password or database is corrupted.")
            return
        
        # Authenticate user
        if self.db_manager.authenticate_user(username, password):
            self.current_user = username
            self.login_successful.emit(username)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password.")
            self.db_manager.close()
    
    def setup_database(self):
        db_password = self.setup_db_password.text().strip()
        db_password_confirm = self.setup_db_password_confirm.text().strip()
        username = self.setup_username.text().strip()
        password = self.setup_password.text().strip()
        password_confirm = self.setup_password_confirm.text().strip()
        
        # Validate inputs
        if not all([db_password, db_password_confirm, username, password, password_confirm]):
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        if db_password != db_password_confirm:
            QMessageBox.warning(self, "Error", "Database passwords do not match.")
            return
        
        if password != password_confirm:
            QMessageBox.warning(self, "Error", "User passwords do not match.")
            return
        
        if len(db_password) < 6:
            QMessageBox.warning(self, "Error", "Database password must be at least 6 characters long.")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "User password must be at least 6 characters long.")
            return
        
        # Initialize database
        if not self.db_manager.initialize_database(db_password):
            QMessageBox.critical(self, "Error", "Failed to create database. Database may already exist.")
            return
        
        # Connect to the new database
        if not self.db_manager.connect(db_password):
            QMessageBox.critical(self, "Error", "Failed to connect to the newly created database.")
            return
        
        # Create the first user
        if self.db_manager.create_user(username, password):
            QMessageBox.information(self, "Success", 
                                  "Database and user created successfully! You can now login.")
            # Switch to login tab
            tab_widget = self.findChild(QTabWidget)
            if tab_widget:
                tab_widget.setCurrentIndex(0)
                # Clear setup fields
                self.setup_db_password.clear()
                self.setup_db_password_confirm.clear()
                self.setup_username.clear()
                self.setup_password.clear()
                self.setup_password_confirm.clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to create user.")
        
        self.db_manager.close()
    
    def get_database_manager(self):
        return self.db_manager
    
    def get_current_user(self):
        return self.current_user
