import sys
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QTabWidget,
                            QWidget, QFormLayout, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from database import DatabaseManager
import os
import json

class LoginDialog(QDialog):
    login_successful = pyqtSignal(str)  # Signal emitted when login is successful
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.current_language = "English"
        
        # Language dictionaries
        self.texts = {
            "English": {
                "title": "Psychological Records Application",
                "window_title": "Psychological Records - Login",
                "db_password": "Database Password",
                "username": "Username",
                "password": "Password",
                "login_button": "Login",
                "setup_button": "Create Database & User",
                "login_tab": "Login",
                "setup_tab": "Initial Setup",
                "db_password_placeholder": "Enter database password",
                "username_placeholder": "Enter username",
                "password_placeholder": "Enter password",
                "create_db_password_placeholder": "Create database password",
                "confirm_db_password": "Confirm DB Password",
                "user_password": "User Password",
                "confirm_password": "Confirm Password",
                "fill_all_fields": "Please fill in all fields.",
                "passwords_no_match": "Database passwords do not match.",
                "user_passwords_no_match": "User passwords do not match.",
                "password_too_short": "Password must be at least 6 characters long.",
                "invalid_db_password": "Invalid database password or database is corrupted.",
                "invalid_credentials": "Invalid username or password.",
                "user_creation_success": "Database and user created successfully! You can now login.",
                "user_creation_failed": "Failed to create user."
            },
            "Română": {
                "title": "Aplicația de Înregistrări Psihologice",
                "window_title": "Înregistrări Psihologice - Autentificare",
                "db_password": "Parola Bazei de Date",
                "username": "Nume Utilizator",
                "password": "Parola",
                "login_button": "Autentificare",
                "setup_button": "Creează Baza de Date și Utilizator",
                "login_tab": "Autentificare",
                "setup_tab": "Configurare Inițială",
                "db_password_placeholder": "Introduceți parola bazei de date",
                "username_placeholder": "Introduceți numele de utilizator",
                "password_placeholder": "Introduceți parola",
                "create_db_password_placeholder": "Creați parola bazei de date",
                "confirm_db_password": "Confirmați Parola BD",
                "user_password": "Parola Utilizator",
                "confirm_password": "Confirmați Parola",
                "fill_all_fields": "Vă rugăm să completați toate câmpurile.",
                "passwords_no_match": "Parolele bazei de date nu se potrivesc.",
                "user_passwords_no_match": "Parolele utilizatorului nu se potrivesc.",
                "password_too_short": "Parola trebuie să aibă cel puțin 6 caractere.",
                "invalid_db_password": "Parola bazei de date este invalidă sau baza de date este coruptă.",
                "invalid_credentials": "Nume de utilizator sau parolă invalidă.",
                "user_creation_success": "Baza de date și utilizatorul au fost create cu succes! Acum vă puteți autentifica.",
                "user_creation_failed": "Eșuarea creării utilizatorului."
            }
        }
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Psychological Records - Login / Înregistrări Psihologice - Autentificare")
        self.setFixedSize(600, 550)
        self.setModal(True)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Language selector
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language / Limbă:")
        lang_label.setStyleSheet("font-weight: 600; color: #495057; font-size: 12px;")
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Română"])
        self.language_combo.setCurrentText("English")
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.language_combo.setMaximumWidth(150)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        main_layout.addLayout(lang_layout)
        
        # Title
        self.title_label = QLabel("Psychological Records Application")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #2c3e50; 
            margin: 25px; 
            padding: 20px;
            background-color: #e8f4f8;
            border-radius: 10px;
            border: 2px solid #0d6efd;
        """)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Login tab
        login_tab = QWidget()
        login_layout = QFormLayout()
        login_layout.setSpacing(20)
        login_layout.setContentsMargins(30, 20, 30, 20)
        
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
                background-color: #198754;
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 16px;
                min-height: 30px;
                min-width: 150px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #157347;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(25, 135, 84, 0.3);
            }
            QPushButton:pressed {
                background-color: #146c43;
                transform: translateY(0px);
            }
        """)
        
        login_layout.addRow("", login_button)
        login_tab.setLayout(login_layout)
        
        # Setup tab
        setup_tab = QWidget()
        setup_layout = QFormLayout()
        setup_layout.setSpacing(20)
        setup_layout.setContentsMargins(30, 20, 30, 20)
        
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
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 16px;
                min-height: 30px;
                min-width: 200px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(13, 110, 253, 0.3);
            }
            QPushButton:pressed {
                background-color: #0a58ca;
                transform: translateY(0px);
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
        
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(tab_widget)
        
        self.setLayout(main_layout)
        
        # Connect Enter key to login
        self.password_input.returnPressed.connect(self.login)
        self.db_password_input.returnPressed.connect(self.login)
        
        # Apply enhanced stylesheet with better visibility
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #212529;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                padding: 16px 20px;
                border: 3px solid #6c757d;
                border-radius: 10px;
                font-size: 16px;
                background-color: white;
                color: #212529;
                selection-background-color: #0d6efd;
                selection-color: white;
                min-height: 25px;
                font-weight: 500;
                margin: 5px 0px;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
                box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.15);
            }
            QLineEdit::placeholder {
                color: #6c757d;
                font-style: italic;
                font-weight: 400;
            }
            QLabel {
                font-weight: 700;
                color: #495057;
                font-size: 15px;
                padding: 8px 0px;
                margin: 5px 0px;
            }
            QTabWidget::pane {
                border: 3px solid #dee2e6;
                background-color: white;
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 15px 30px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                color: #495057;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 4px solid #0d6efd;
                color: #0d6efd;
                font-weight: 700;
                font-size: 15px;
            }
            QTabBar::tab:hover {
                background-color: #dee2e6;
                color: #212529;
            }
            QFormLayout {
                margin: 20px;
                spacing: 15px;
            }
        """)
    
    def get_text(self, key):
        """Get text in current language."""
        return self.texts[self.current_language].get(key, key)
    
    def change_language(self, language):
        """Change the interface language."""
        self.current_language = language
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        self.setWindowTitle(self.get_text("window_title"))
        self.title_label.setText(self.get_text("title"))
        
        # Update placeholders
        self.db_password_input.setPlaceholderText(self.get_text("db_password_placeholder"))
        self.username_input.setPlaceholderText(self.get_text("username_placeholder"))
        self.password_input.setPlaceholderText(self.get_text("password_placeholder"))
        
        # Update setup placeholders
        self.setup_db_password.setPlaceholderText(self.get_text("create_db_password_placeholder"))
        
        # Update buttons
        if hasattr(self, 'login_button'):
            self.login_button.setText(self.get_text("login_button"))
        if hasattr(self, 'setup_button'):
            self.setup_button.setText(self.get_text("setup_button"))
        
        # Update tab labels
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setTabText(0, self.get_text("login_tab"))
            if self.tab_widget.count() > 1:
                self.tab_widget.setTabText(1, self.get_text("setup_tab"))
    
    def login(self):
        db_password = self.db_password_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not all([db_password, username, password]):
            QMessageBox.warning(self, "Error", self.get_text("fill_all_fields"))
            return
        
        # Try to connect to database
        if not self.db_manager.connect(db_password):
            QMessageBox.critical(self, "Error", self.get_text("invalid_db_password"))
            return
        
        # Authenticate user
        if self.db_manager.authenticate_user(username, password):
            self.current_user = username
            self.login_successful.emit(username)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", self.get_text("invalid_credentials"))
            self.db_manager.close()
    
    def setup_database(self):
        db_password = self.setup_db_password.text().strip()
        db_password_confirm = self.setup_db_password_confirm.text().strip()
        username = self.setup_username.text().strip()
        password = self.setup_password.text().strip()
        password_confirm = self.setup_password_confirm.text().strip()
        
        # Validate inputs
        if not all([db_password, db_password_confirm, username, password, password_confirm]):
            QMessageBox.warning(self, "Error", self.get_text("fill_all_fields"))
            return
        
        if db_password != db_password_confirm:
            QMessageBox.warning(self, "Error", self.get_text("passwords_no_match"))
            return
        
        if password != password_confirm:
            QMessageBox.warning(self, "Error", self.get_text("user_passwords_no_match"))
            return
        
        if len(db_password) < 6:
            QMessageBox.warning(self, "Error", self.get_text("password_too_short"))
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", self.get_text("password_too_short"))
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
            QMessageBox.information(self, "Success", self.get_text("user_creation_success"))
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
            QMessageBox.critical(self, "Error", self.get_text("user_creation_failed"))
        
        self.db_manager.close()
    
    def get_database_manager(self):
        return self.db_manager
    
    def get_current_user(self):
        return self.current_user
