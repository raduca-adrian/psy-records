import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QLabel, QHeaderView, QMenuBar, 
                            QMenu, QStatusBar, QToolBar, QLineEdit, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont
from src.ui.person_dialog import PersonDialog
from src.ui.change_password_dialog import ChangePasswordDialog
from src.utils.app_translator import get_text
from src.utils.language_manager import get_language_manager, get_text as lang_get_text
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, db_manager, username):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
        self.language_manager = get_language_manager()
        # Register for language change notifications
        self.language_manager.register_language_change_callback(self.on_language_updated)
        self.init_ui()
        self.load_persons()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_persons)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def init_ui(self):
        self.setWindowTitle(f"Secure Database Application - Welcome, {self.username}")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header with enhanced styling
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel(self.get_text('main_window.title'))
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #000000;
                padding: 15px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #e9ecef, stop:1 #f8f9fa);
                border-radius: 10px;
                border: 2px solid #dee2e6;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
        """)
        
        user_label = QLabel(f"👤 {self.get_text('main_window.logged_in_as')}: {self.username}")
        user_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-weight: 700;
                background-color: #e9ecef;
                padding: 10px 16px;
                border-radius: 20px;
                border: 2px solid #dee2e6;
                margin: 8px;
                font-size: 13px;
                min-width: 150px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
        """)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(user_label)
        
        # Search bar with enhanced styling
        search_layout = QHBoxLayout()
        self.search_label = QLabel(f"🔍 {self.get_text('main_window.search')}:")
        self.search_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-weight: 800;
                font-size: 14px;
                margin-right: 12px;
                padding: 8px;
                background-color: #e9ecef;
                border-radius: 6px;
                min-width: 80px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
        """)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.get_text('main_window.search_placeholder'))
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input.setMaximumWidth(400)
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 20px;
                border: 3px solid #ced4da;
                border-radius: 10px;
                font-size: 14px;
                background-color: white;
                color: #000000;
                selection-background-color: #0d6efd;
                selection-color: white;
                font-weight: 600;
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
        """)
        
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton(f"➕ {self.get_text('main_window.add_person')}")
        self.add_button.clicked.connect(self.add_person)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #198754;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
                min-width: 120px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
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
        
        self.edit_button = QPushButton(f"✏️ {self.get_text('main_window.edit_person')}")
        self.edit_button.clicked.connect(self.edit_person)
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
                min-width: 120px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
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
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
                transform: none;
                box-shadow: none;
            }
        """)
        
        self.delete_button = QPushButton(f"🗑️ {self.get_text('main_window.delete_person')}")
        self.delete_button.clicked.connect(self.delete_person)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
                min-width: 120px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #bb2d3b;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
            }
            QPushButton:pressed {
                background-color: #b02a37;
                transform: translateY(0px);
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
                transform: none;
                box-shadow: none;
            }
        """)
        
        self.refresh_button = QPushButton(f"🔄 {self.get_text('main_window.refresh')}")
        self.refresh_button.clicked.connect(self.load_persons)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
                min-width: 120px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #e8650e;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(253, 126, 20, 0.3);
            }
            QPushButton:pressed {
                background-color: #dc5f0d;
                transform: translateY(0px);
            }
        """)
        
        self.medical_records_button = QPushButton(f"🧠 {self.get_text('main_window.psychological_records')}")
        self.medical_records_button.clicked.connect(self.open_medical_records)
        self.medical_records_button.setEnabled(False)
        self.medical_records_button.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
                min-width: 140px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #5a359a;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(111, 66, 193, 0.3);
            }
            QPushButton:pressed {
                background-color: #4c2d83;
                transform: translateY(0px);
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
                transform: none;
                box-shadow: none;
            }
        """)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.medical_records_button)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            self.get_text('main_window.id'), 
            self.get_text('main_window.name'), 
            self.get_text('main_window.cnp'), 
            self.get_text('main_window.created')
        ])
        
        # Hide ID column
        self.table.setColumnHidden(0, True)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Table selection
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.edit_person)
        
        # Enhanced table styling with better visibility
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #dee2e6;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #cce7ff;
                selection-color: #000000;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f1f3f4;
                border-right: 1px solid #f8f9fa;
                color: #000000;
                font-weight: 600;
            }
            QTableWidget::item:selected {
                background-color: #cce7ff;
                color: #000000;
                border: 2px solid #0d6efd;
                font-weight: 700;
            }
            QTableWidget::item:hover {
                background-color: #e3f2fd;
                color: #000000;
                font-weight: 700;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                color: #000000;
                padding: 15px 10px;
                border: none;
                border-right: 1px solid #dee2e6;
                border-bottom: 2px solid #0d6efd;
                font-weight: 800;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QHeaderView::section:hover {
                background-color: #dee2e6;
                color: #000000;
            }
        """)
        self.table.setAlternatingRowColors(True)
        
        # Add layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        central_widget.setLayout(main_layout)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.get_text('main_window.ready'))
        
        # Apply initial translations
        self.update_ui_texts()
        
        # Apply enhanced main window styling for better visibility
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                color: #000000;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMenuBar {
                background-color: #e9ecef;
                color: #000000;
                border-bottom: 1px solid #dee2e6;
                padding: 4px;
                font-weight: 600;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #000000;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: 600;
            }
            QMenuBar::item:selected {
                background-color: #0d6efd;
                color: white;
                font-weight: 700;
            }
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 16px;
                color: #000000;
                border-radius: 4px;
                font-weight: 600;
            }
            QMenu::item:selected {
                background-color: #0d6efd;
                color: white;
                font-weight: 700;
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
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                background-color: #e9ecef;
            }
            QComboBox::drop-down:hover {
                background-color: #dee2e6;
            }
            QComboBox::down-arrow {
                image: none;
                border: 3px solid #000000;
                width: 10px;
                height: 10px;
                border-top: none;
                border-right: none;
                transform: rotate(45deg);
                margin-top: -3px;
            }
            QComboBox QAbstractItemView {
                border: 3px solid #0d6efd;
                background-color: white;
                color: #000000;
                selection-background-color: #0d6efd;
                selection-color: white;
                font-size: 16px;
                padding: 8px;
                outline: none;
                font-weight: 600;
                min-width: 200px;
            }
            QComboBox QAbstractItemView::item {
                padding: 16px 20px;
                color: #000000;
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
                color: #000000;
                font-weight: 700;
            }
            QLabel {
                color: #212529;
                font-weight: 700;
                font-size: 16px;
                padding: 10px 4px;
                min-height: 32px;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                selection-background-color: #cce7ff;
                selection-color: #000000;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
                color: #000000;
                font-weight: 600;
            }
            QTableWidget::item:selected {
                background-color: #cce7ff;
                color: #000000;
                font-weight: 700;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                color: #000000;
                padding: 10px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: 700;
                font-size: 12px;
            }
            QHeaderView::section:hover {
                background-color: #dee2e6;
                color: #000000;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 700;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ffffff;
                font-weight: 700;
            }
            QLabel {
                color: #000000;
                font-weight: 600;
            }
            QStatusBar {
                background-color: #e9ecef;
                color: #000000;
                border-top: 1px solid #dee2e6;
                padding: 4px;
                font-weight: 600;
            }
        """)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        self.file_menu = menubar.addMenu(self.get_text('menu.file'))
        
        self.refresh_action = QAction(self.get_text('menu.refresh'), self)
        self.refresh_action.setShortcut('F5')
        self.refresh_action.triggered.connect(self.load_persons)
        self.file_menu.addAction(self.refresh_action)
        
        self.file_menu.addSeparator()
        
        self.exit_action = QAction(self.get_text('menu.exit'), self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)
        
        # Edit menu
        self.edit_menu = menubar.addMenu(self.get_text('menu.edit'))
        
        self.add_person_action = QAction(self.get_text('menu.add_person'), self)
        self.add_person_action.setShortcut('Ctrl+N')
        self.add_person_action.triggered.connect(self.add_person)
        self.edit_menu.addAction(self.add_person_action)
        
        self.edit_person_action = QAction(self.get_text('menu.edit_person'), self)
        self.edit_person_action.setShortcut('Ctrl+E')
        self.edit_person_action.triggered.connect(self.edit_person)
        self.edit_menu.addAction(self.edit_person_action)
        
        self.delete_person_action = QAction(self.get_text('menu.delete_person'), self)
        self.delete_person_action.setShortcut('Delete')
        self.delete_person_action.triggered.connect(self.delete_person)
        self.edit_menu.addAction(self.delete_person_action)
        
        # Account menu
        self.account_menu = menubar.addMenu(self.get_text('menu.account'))
        
        self.change_password_action = QAction(self.get_text('menu.change_password'), self)
        self.change_password_action.triggered.connect(self.change_password)
        self.account_menu.addAction(self.change_password_action)
        
        # Language menu
        self.language_menu = menubar.addMenu(self.get_text('menu.language'))
        self.create_language_menu()
    
    def create_language_menu(self):
        """Create language selection menu."""
        self.language_menu.clear()
        
        # Create language action group for radio button behavior
        from PyQt6.QtGui import QActionGroup
        self.language_action_group = QActionGroup(self)
        
        current_language = self.language_manager.get_current_language()
        
        for locale in self.language_manager.get_available_languages():
            display_name = self.language_manager.get_language_display_name(locale)
            action = QAction(display_name, self)
            action.setCheckable(True)
            action.setChecked(locale == current_language)
            action.setData(locale)
            action.triggered.connect(lambda checked, loc=locale: self.change_app_language(loc))
            
            self.language_action_group.addAction(action)
            self.language_menu.addAction(action)
    
    def change_app_language(self, locale: str):
        """Change the application language."""
        if self.language_manager.change_language(locale):
            # Update the language menu to reflect the change
            self.create_language_menu()
    
    def load_persons(self):
        """Load all persons from database into the table"""
        try:
            persons = self.db_manager.get_all_persons()
            self.table.setRowCount(len(persons))
            
            for row, person in enumerate(persons):
                # ID (hidden)
                self.table.setItem(row, 0, QTableWidgetItem(str(person[0])))
                # Name
                self.table.setItem(row, 1, QTableWidgetItem(person[1]))
                # CNP
                self.table.setItem(row, 2, QTableWidgetItem(person[2]))
                # Created date (formatted)
                created_date = datetime.fromisoformat(person[3].replace('Z', '+00:00'))
                formatted_date = created_date.strftime('%Y-%m-%d %H:%M')
                self.table.setItem(row, 3, QTableWidgetItem(formatted_date))
            
            self.status_bar.showMessage(f"Loaded {len(persons)} persons")
            
        except Exception as e:
            QMessageBox.critical(self, self.get_text('common.error'), f"{self.get_text('main_window.error_loading')}: {str(e)}")
            self.status_bar.showMessage(self.get_text('main_window.error_loading_status'))
    
    def filter_table(self, text):
        """Filter table based on search text"""
        for row in range(self.table.rowCount()):
            match = False
            # Check name and CNP columns
            for col in [1, 2]:  # Name and CNP columns
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)
    
    def on_selection_changed(self):
        """Enable/disable buttons based on selection"""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.medical_records_button.setEnabled(has_selection)
    
    def get_selected_person(self):
        """Get the currently selected person data"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            person_id = int(self.table.item(current_row, 0).text())
            name = self.table.item(current_row, 1).text()
            cnp = self.table.item(current_row, 2).text()
            created = self.table.item(current_row, 3).text()
            return (person_id, name, cnp, created)
        return None
    
    def add_person(self):
        """Open dialog to add a new person"""
        dialog = PersonDialog(self.db_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_persons()
    
    def edit_person(self):
        """Open dialog to edit selected person"""
        person_data = self.get_selected_person()
        if person_data:
            dialog = PersonDialog(self.db_manager, person_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_persons()
        else:
            QMessageBox.warning(self, self.get_text('common.warning'), self.get_text('main_window.select_person_edit'))
    
    def delete_person(self):
        """Delete the selected person"""
        person_data = self.get_selected_person()
        if person_data:
            reply = QMessageBox.question(
                self, 
                "Confirm Delete", 
                f"Are you sure you want to delete {person_data[1]} (CNP: {person_data[2]})?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self.db_manager.delete_person(person_data[0]):
                    self.load_persons()
                    self.status_bar.showMessage("Person deleted successfully")
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete person.")
        else:
            QMessageBox.warning(self, self.get_text('common.warning'), self.get_text('main_window.select_person_delete'))
    
    def change_password(self):
        """Open dialog to change password"""
        dialog = ChangePasswordDialog(self.db_manager, self.username)
        dialog.exec()
    
    def open_medical_records(self):
        """Open psychological records window for selected person"""
        person_data = self.get_selected_person()
        if person_data:
            # Import here to avoid circular imports
            from src.ui.medical_records_window import MedicalRecordsWindow
            
            # Create and show psychological records window
            records_window = MedicalRecordsWindow(person_data, self.db_manager, self)
            records_window.show()
        else:
            QMessageBox.warning(self, self.get_text('common.warning'), self.get_text('main_window.select_person_records'))
    
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.refresh_timer.stop()
            self.db_manager.close()
            event.accept()
        else:
            event.ignore()
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)
    
    def on_language_updated(self, locale: str):
        """Called when language is changed from anywhere in the application."""
        self.update_ui_texts()
        # Refresh the persons table to update any displayed text
        self.load_persons()
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        self.setWindowTitle(f"{self.get_text('main_window.title')} - {self.get_text('main_window.logged_in_as')}, {self.username}")
        
        # Update main interface elements
        try:
            self.title_label.setText(self.get_text('main_window.title'))
        except AttributeError:
            pass
        
        # Update search elements
        try:
            self.search_label.setText(self.get_text('main_window.search'))
            self.search_input.setPlaceholderText(self.get_text('main_window.search_placeholder'))
        except AttributeError:
            pass
        
        # Update buttons
        try:
            self.add_button.setText(self.get_text('main_window.add_person'))
            self.edit_button.setText(self.get_text('main_window.edit_person'))
            self.delete_button.setText(self.get_text('main_window.delete_person'))
            self.medical_records_button.setText(self.get_text('main_window.psychological_records'))
            self.refresh_button.setText(self.get_text('main_window.refresh'))
        except AttributeError:
            pass
        
        # Update table headers
        try:
            self.table.setHorizontalHeaderLabels([
                self.get_text('main_window.id'),
                self.get_text('main_window.name'),
                self.get_text('main_window.cnp'),
                self.get_text('main_window.created')
            ])
        except AttributeError:
            pass
        
        # Update menu items
        self.update_menu_texts()
        
        # Update status bar
        try:
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage(self.get_text('main_window.ready'))
        except AttributeError:
            pass
    
    def update_menu_texts(self):
        """Update menu item texts."""
        try:
            # Update File menu
            self.file_menu.setTitle(self.get_text('menu.file'))
            self.refresh_action.setText(self.get_text('menu.refresh'))
            self.exit_action.setText(self.get_text('menu.exit'))
            
            # Update Edit menu  
            self.edit_menu.setTitle(self.get_text('menu.edit'))
            self.add_person_action.setText(self.get_text('menu.add_person'))
            self.edit_person_action.setText(self.get_text('menu.edit_person'))
            self.delete_person_action.setText(self.get_text('menu.delete_person'))
            
            # Update Account menu
            self.account_menu.setTitle(self.get_text('menu.account'))
            self.change_password_action.setText(self.get_text('menu.change_password'))
            
            # Update Language menu
            self.language_menu.setTitle(self.get_text('menu.language'))
            # Recreate language menu to update display names
            self.create_language_menu()
        except AttributeError:
            pass
        