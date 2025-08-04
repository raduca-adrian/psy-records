import sys
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QTabWidget,
                            QWidget, QFormLayout, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from database import DatabaseManager
from src.utils.app_translator import get_text, set_language, get_available_locales, get_translator
import os
import json

class LoginDialog(QDialog):
    login_successful = pyqtSignal(str)  # Signal emitted when login is successful
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.load_saved_language()
        self.init_ui()
    
    def load_saved_language(self):
        """Load saved language preference."""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    saved_locale = settings.get('language', 'en')
                    set_language(saved_locale)
        except Exception:
            set_language('en')  # Default to English
    
    def save_language_preference(self, locale):
        """Save language preference to settings file."""
        try:
            settings = {}
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            settings['language'] = locale
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save language preference: {e}")
    
    def get_text(self, key):
        """Get translated text."""
        return get_text(key, key)
    
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
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Română", "ro")
        
        # Set current language based on saved preference
        current_locale = get_translator().locale
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_locale:
                self.language_combo.setCurrentIndex(i)
                break
        
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
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
        self.tab_widget = QTabWidget()
        
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
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("""
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
        
        login_layout.addRow("", self.login_button)
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
        
        self.setup_button = QPushButton("Create Database & User")
        self.setup_button.clicked.connect(self.setup_database)
        self.setup_button.setStyleSheet("""
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
        
        setup_layout.addRow("", self.setup_button)
        setup_tab.setLayout(setup_layout)
        
        # Add tabs
        self.tab_widget.addTab(login_tab, "Login")
        
        # Only show setup tab if database doesn't exist
        if not os.path.exists("secure_app.db.enc"):
            self.tab_widget.addTab(setup_tab, "Initial Setup")
            self.tab_widget.setCurrentIndex(1)  # Start with setup tab
        
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.tab_widget)
        
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
                padding: 18px 20px;
                border: 3px solid #6c757d;
                border-radius: 10px;
                font-size: 16px;
                background-color: white;
                color: #212529;
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
                color: #6c757d;
                font-style: italic;
                font-weight: 500;
            }
            QLabel {
                font-weight: 700;
                color: #495057;
                font-size: 16px;
                padding: 10px 0px;
                margin: 6px 0px;
                min-height: 30px;
            }
            QComboBox {
                padding: 18px 20px;
                border: 3px solid #6c757d;
                border-radius: 10px;
                font-size: 16px;
                background-color: white;
                color: #212529;
                min-height: 30px;
                max-height: 60px;
                font-weight: 600;
                margin: 6px 0px;
            }
            QComboBox:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
                box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.15);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 32px;
                border-left: 3px solid #6c757d;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: #e9ecef;
            }
            QComboBox::drop-down:hover {
                background-color: #dee2e6;
            }
            QComboBox::down-arrow {
                image: none;
                border: 3px solid #212529;
                width: 10px;
                height: 10px;
                border-top: none;
                border-right: none;
                margin-top: -3px;
            }
            QComboBox QAbstractItemView {
                border: 3px solid #0d6efd;
                background-color: white;
                color: #212529;
                selection-background-color: #0d6efd;
                selection-color: white;
                font-size: 16px;
                padding: 8px;
                outline: none;
                font-weight: 600;
            }
            QComboBox QAbstractItemView::item {
                padding: 18px 20px;
                color: #212529;
                background-color: white;
                border: none;
                min-height: 35px;
                font-weight: 600;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #0d6efd;
                color: white;
                font-weight: 700;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #cce7ff;
                color: #212529;
                font-weight: 700;
            }
            QTabWidget::pane {
                border: 3px solid #dee2e6;
                background-color: white;
                border-radius: 10px;
                margin-top: 10px;
                padding: 20px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 18px 35px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                color: #495057;
                font-weight: 700;
                font-size: 15px;
                min-width: 130px;
                min-height: 25px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 4px solid #0d6efd;
                color: #0d6efd;
                font-weight: 700;
                font-size: 16px;
            }
            QTabBar::tab:hover {
                background-color: #dee2e6;
                color: #212529;
            }
            QFormLayout {
                margin: 25px;
                spacing: 20px;
            }
        """)
    
    def on_language_changed(self):
        """Handle language change from combo box."""
        current_index = self.language_combo.currentIndex()
        locale = self.language_combo.itemData(current_index)
        if locale:
            set_language(locale)
            self.save_language_preference(locale)
            self.update_ui_texts()
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        # Update window title and main label
        self.setWindowTitle(self.get_text("login.title"))
        
        try:
            self.title_label.setText(self.get_text("app.title"))
        except (AttributeError, RuntimeError):
            pass
        
        # Update login form placeholders with error handling
        try:
            self.db_password_input.setPlaceholderText(self.get_text("login.db_password_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.username_input.setPlaceholderText(self.get_text("login.username_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.password_input.setPlaceholderText(self.get_text("login.password_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        
        # Update setup form placeholders with error handling
        try:
            self.setup_db_password.setPlaceholderText(self.get_text("login.create_db_password_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.setup_db_password_confirm.setPlaceholderText(self.get_text("login.confirm_db_password_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.setup_username.setPlaceholderText(self.get_text("login.create_username_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.setup_password.setPlaceholderText(self.get_text("login.create_password_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.setup_password_confirm.setPlaceholderText(self.get_text("login.confirm_password_placeholder"))
        except (AttributeError, RuntimeError):
            pass
        
        # Update buttons with error handling
        try:
            self.login_button.setText(self.get_text("login.login_button"))
        except (AttributeError, RuntimeError):
            pass
        try:
            self.setup_button.setText(self.get_text("login.setup_button"))
        except (AttributeError, RuntimeError):
            pass
        
        # Update tab labels with error handling
        try:
            self.tab_widget.setTabText(0, self.get_text("login.login_tab"))
            if self.tab_widget.count() > 1:
                self.tab_widget.setTabText(1, self.get_text("login.setup_tab"))
        except (AttributeError, RuntimeError):
            pass
    
    def login(self):
        db_password = self.db_password_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not all([db_password, username, password]):
            QMessageBox.warning(self, self.get_text("login.error"), 
                              self.get_text("login.fill_all_fields"))
            return
        
        # Try to connect to database
        if not self.db_manager.connect(db_password):
            QMessageBox.critical(self, self.get_text("login.error"), 
                               self.get_text("login.invalid_db_password"))
            return
        
        # Authenticate user
        if self.db_manager.authenticate_user(username, password):
            self.current_user = username
            self.login_successful.emit(username)
            self.accept()
        else:
            QMessageBox.critical(self, self.get_text("login.error"), 
                               self.get_text("login.invalid_credentials"))
            self.db_manager.close()
    
    def setup_database(self):
        db_password = self.setup_db_password.text().strip()
        db_password_confirm = self.setup_db_password_confirm.text().strip()
        username = self.setup_username.text().strip()
        password = self.setup_password.text().strip()
        password_confirm = self.setup_password_confirm.text().strip()
        
        # Validate inputs
        if not all([db_password, db_password_confirm, username, password, password_confirm]):
            QMessageBox.warning(self, self.get_text("login.error"), self.get_text("login.fill_all_fields"))
            return
        
        if db_password != db_password_confirm:
            QMessageBox.warning(self, self.get_text("login.error"), self.get_text("login.passwords_no_match"))
            return
        
        if password != password_confirm:
            QMessageBox.warning(self, self.get_text("login.error"), self.get_text("login.user_passwords_no_match"))
            return
        
        if len(db_password) < 6:
            QMessageBox.warning(self, self.get_text("login.error"), self.get_text("login.db_password_too_short"))
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, self.get_text("login.error"), self.get_text("login.password_too_short"))
            return
        
        # Initialize database
        if not self.db_manager.initialize_database(db_password):
            QMessageBox.critical(self, self.get_text("login.error"), self.get_text("login.db_creation_failed"))
            return
        
        # Connect to the new database
        if not self.db_manager.connect(db_password):
            QMessageBox.critical(self, self.get_text("login.error"), self.get_text("login.db_connect_failed"))
            return
        
        # Create the first user
        if self.db_manager.create_user(username, password):
            QMessageBox.information(self, self.get_text("common.success"), self.get_text("login.user_creation_success"))
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
            QMessageBox.critical(self, self.get_text("login.error"), self.get_text("login.user_creation_failed"))
        
        self.db_manager.close()
    
    def get_database_manager(self):
        return self.db_manager
    
    def get_current_user(self):
        return self.current_user
