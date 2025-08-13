import sys
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QTabWidget,
                            QWidget, QFormLayout, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont
from database import DatabaseManager
from src.utils.language_manager import get_language_manager, get_text as lang_get_text
from src.ui.styles import WidgetStyles, StyleHelper
import os
import json

class LoginDialog(QDialog):
    login_successful = pyqtSignal(str)  # Signal emitted when login is successful
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user = None
        self.language_manager = get_language_manager()
        # Register for language change notifications
        self.language_manager.register_language_change_callback(self.on_language_updated)
        self.init_ui()
        # Apply initial language settings after UI is created
        self.update_ui_texts()
    
    def load_saved_language(self):
        """Load saved language preference."""
        # This is now handled by the language manager
        pass
    
    def save_language_preference(self, locale):
        """Save language preference to settings file."""
        # This is now handled by the language manager
        return self.language_manager.save_language_preference(locale)
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)
    
    def init_ui(self):
        self.setWindowTitle("Psychological Records - Login / Înregistrări Psihologice - Autentificare")
        # Using centralized dimension management
        WidgetStyles.apply_dialog_dimensions(self)
        self.setModal(True)
        
        # Create main layout
        main_layout = QVBoxLayout()
        
        # Language selector
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Language / Limbă:")
        WidgetStyles.apply_language_label(self.lang_label)
        
        self.language_combo = QComboBox()
        # Populate combo box with available languages
        for locale in self.language_manager.get_available_languages():
            display_name = self.language_manager.get_language_display_name(locale)
            self.language_combo.addItem(display_name, locale)
        
        # Set current language based on saved preference
        current_locale = self.language_manager.get_current_language()
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_locale:
                self.language_combo.setCurrentIndex(i)
                break
        
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        # Using centralized sizing management
        WidgetStyles.apply_combo_sizing(self.language_combo)
        
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        main_layout.addLayout(lang_layout)
        
        # Title
        self.title_label = QLabel("Psychological Records Application")
        # Using centralized typography instead of manual font setting
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        WidgetStyles.apply_title_label(self.title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Login tab
        login_tab = QWidget()
        login_layout = QFormLayout()
        # Using centralized spacing instead of hardcoded values
        WidgetStyles.apply_form_layout(login_layout)
        
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.db_password_input.setPlaceholderText("Enter database password")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        
        # Create labels for form rows to enable translation
        self.db_password_label = QLabel("Database Password:")
        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")
        
        login_layout.addRow(self.db_password_label, self.db_password_input)
        login_layout.addRow(self.username_label, self.username_input)
        login_layout.addRow(self.password_label, self.password_input)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        WidgetStyles.apply_success_button(self.login_button)
        
        login_layout.addRow("", self.login_button)
        login_tab.setLayout(login_layout)
        
        # Setup tab
        setup_tab = QWidget()
        setup_layout = QFormLayout()
        # Using centralized spacing instead of hardcoded values
        WidgetStyles.apply_form_layout(setup_layout)
        
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
        
        # Create labels for setup form rows to enable translation
        self.setup_db_password_label = QLabel("Database Password:")
        self.setup_db_password_confirm_label = QLabel("Confirm DB Password:")
        self.setup_username_label = QLabel("Username:")
        self.setup_password_label = QLabel("User Password:")
        self.setup_password_confirm_label = QLabel("Confirm Password:")
        
        setup_layout.addRow(self.setup_db_password_label, self.setup_db_password)
        setup_layout.addRow(self.setup_db_password_confirm_label, self.setup_db_password_confirm)
        setup_layout.addRow(self.setup_username_label, self.setup_username)
        setup_layout.addRow(self.setup_password_label, self.setup_password)
        setup_layout.addRow(self.setup_password_confirm_label, self.setup_password_confirm)
        
        self.setup_button = QPushButton("Create Database & User")
        self.setup_button.clicked.connect(self.setup_database)
        WidgetStyles.apply_primary_button_wide(self.setup_button)
        
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
        
        # Apply centralized styling system
        WidgetStyles.apply_dialog_style(self)
    
    def on_language_changed(self):
        """Handle language change from combo box."""
        current_index = self.language_combo.currentIndex()
        locale = self.language_combo.itemData(current_index)
        if locale and locale != self.language_manager.get_current_language():
            self.language_manager.change_language(locale)
    
    def on_language_updated(self, locale: str):
        """Called when language is changed from anywhere in the application."""
        # Update combo box selection if needed
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == locale:
                if self.language_combo.currentIndex() != i:
                    self.language_combo.setCurrentIndex(i)
                break
        
        # Update all UI texts
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        # Update window title and main label
        self.setWindowTitle(self.get_text("login.title"))
        
        try:
            self.title_label.setText(self.get_text("app.title"))
        except (AttributeError, RuntimeError):
            pass
        
        # Update language label (add a simple bilingual label since translation key doesn't exist)
        try:
            self.lang_label.setText("Language / Limbă:")
        except (AttributeError, RuntimeError):
            pass
        
        # Update login form labels (using existing translation keys)
        try:
            self.db_password_label.setText(self.get_text("login.database_password"))
            self.username_label.setText(self.get_text("login.username"))
            self.password_label.setText(self.get_text("login.password"))
        except (AttributeError, RuntimeError):
            pass
        
        # Update setup form labels (using existing translation keys)
        try:
            self.setup_db_password_label.setText(self.get_text("login.database_password"))
            self.setup_db_password_confirm_label.setText(self.get_text("login.confirm_db_password"))
            self.setup_username_label.setText(self.get_text("login.username"))
            self.setup_password_label.setText(self.get_text("login.user_password"))
            self.setup_password_confirm_label.setText(self.get_text("login.confirm_password"))
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
    
    def closeEvent(self, event):
        """Clean up when dialog is closed."""
        # Unregister language change callback
        if hasattr(self, 'language_manager'):
            self.language_manager.unregister_language_change_callback(self.on_language_updated)
        super().closeEvent(event)
