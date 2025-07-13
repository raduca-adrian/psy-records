import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QLabel, QHeaderView, QMenuBar, 
                            QMenu, QStatusBar, QToolBar, QLineEdit, QDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont
from person_dialog import PersonDialog
from change_password_dialog import ChangePasswordDialog
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self, db_manager, username):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
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
        
        title_label = QLabel("PersonDB - Secure Database Manager")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: #212529;
                padding: 15px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #e9ecef, stop:1 #f8f9fa);
                border-radius: 10px;
                border: 2px solid #dee2e6;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """)
        
        user_label = QLabel(f"👤 Logged in as: {self.username}")
        user_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-weight: 600;
                background-color: #e9ecef;
                padding: 10px 16px;
                border-radius: 20px;
                border: 2px solid #dee2e6;
                margin: 8px;
                font-size: 13px;
                min-width: 150px;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(user_label)
        
        # Search bar with enhanced styling
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        search_label.setStyleSheet("""
            QLabel {
                color: #495057;
                font-weight: 700;
                font-size: 14px;
                margin-right: 12px;
                padding: 8px;
                background-color: #e9ecef;
                border-radius: 6px;
                min-width: 80px;
            }
        """)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or CNP...")
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
                color: #212529;
                selection-background-color: #0d6efd;
                selection-color: white;
                font-weight: 500;
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
        """)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("➕ Add Person")
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
        
        self.edit_button = QPushButton("✏️ Edit Person")
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
        
        self.delete_button = QPushButton("🗑️ Delete Person")
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
        
        self.refresh_button = QPushButton("🔄 Refresh")
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
        
        self.medical_records_button = QPushButton("📋 Medical Records")
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
        self.table.setHorizontalHeaderLabels(["ID", "Name", "CNP", "Created"])
        
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
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f1f3f4;
                border-right: 1px solid #f8f9fa;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                border: 2px solid #0d6efd;
                font-weight: 600;
            }
            QTableWidget::item:hover {
                background-color: #f0f7ff;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                color: #495057;
                padding: 15px 10px;
                border: none;
                border-right: 1px solid #dee2e6;
                border-bottom: 2px solid #0d6efd;
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
        self.status_bar.showMessage("Ready")
        
        # Apply enhanced main window styling for better visibility
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                color: #212529;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMenuBar {
                background-color: #e9ecef;
                color: #212529;
                border-bottom: 1px solid #dee2e6;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #495057;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMenuBar::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QMenu {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 16px;
                color: #495057;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 2px solid #6c757d;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: #212529;
                selection-background-color: #0d6efd;
                selection-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
            }
            QLineEdit::placeholder {
                color: #6c757d;
                font-style: italic;
            }
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #6c757d;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                color: #212529;
                selection-background-color: #0d6efd;
                selection-color: white;
                min-height: 20px;
                font-weight: 500;
            }
            QComboBox:focus {
                border-color: #0d6efd;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 2px solid #6c757d;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #e9ecef;
            }
            QComboBox::drop-down:hover {
                background-color: #dee2e6;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #495057;
                width: 6px;
                height: 6px;
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
                min-width: 150px;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px 12px;
                color: #212529;
                background-color: white;
                border: none;
                min-height: 25px;
                font-weight: 500;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #0d6efd;
                color: white;
                font-weight: 600;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: 600;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f3f4;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                color: #495057;
                padding: 10px;
                border: none;
                border-right: 1px solid #dee2e6;
                font-weight: 600;
                font-size: 12px;
            }
            QHeaderView::section:hover {
                background-color: #dee2e6;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
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
                color: #adb5bd;
            }
            QLabel {
                color: #495057;
                font-weight: 500;
            }
            QStatusBar {
                background-color: #e9ecef;
                color: #495057;
                border-top: 1px solid #dee2e6;
                padding: 4px;
            }
        """)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.load_persons)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        add_action = QAction('Add Person', self)
        add_action.setShortcut('Ctrl+N')
        add_action.triggered.connect(self.add_person)
        edit_menu.addAction(add_action)
        
        edit_action = QAction('Edit Person', self)
        edit_action.setShortcut('Ctrl+E')
        edit_action.triggered.connect(self.edit_person)
        edit_menu.addAction(edit_action)
        
        delete_action = QAction('Delete Person', self)
        delete_action.setShortcut('Delete')
        delete_action.triggered.connect(self.delete_person)
        edit_menu.addAction(delete_action)
        
        # Account menu
        account_menu = menubar.addMenu('Account')
        
        change_password_action = QAction('Change Password', self)
        change_password_action.triggered.connect(self.change_password)
        account_menu.addAction(change_password_action)
    
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
            QMessageBox.critical(self, "Error", f"Failed to load persons: {str(e)}")
            self.status_bar.showMessage("Error loading data")
    
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
            QMessageBox.warning(self, "Warning", "Please select a person to edit.")
    
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
            QMessageBox.warning(self, "Warning", "Please select a person to delete.")
    
    def change_password(self):
        """Open dialog to change password"""
        dialog = ChangePasswordDialog(self.db_manager, self.username)
        dialog.exec()
    
    def open_medical_records(self):
        """Open medical records window for selected person"""
        person_data = self.get_selected_person()
        if person_data:
            # Import here to avoid circular imports
            from medical_records_window import MedicalRecordsWindow
            
            # Create and show medical records window
            records_window = MedicalRecordsWindow(person_data, self.db_manager, self)
            records_window.show()
        else:
            QMessageBox.warning(self, "Warning", "Please select a person to view medical records.")
    
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
