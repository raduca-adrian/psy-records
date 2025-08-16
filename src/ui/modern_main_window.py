"""
Enhanced Main Window with responsive design and modern QSS styling.
"""

import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QLabel, QHeaderView, QMenuBar, 
                            QMenu, QStatusBar, QToolBar, QLineEdit, QDialog,
                            QFrame, QSplitter, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QAction, QIcon, QFont, QResizeEvent

from src.ui.responsive_layout import (ResponsiveWidget, FlexibleLayout, 
                                    ResponsiveBreakpoints, LayoutUtils)
from src.ui.modern_qss import get_style_manager
from src.ui.person_dialog import PersonDialog
from src.ui.change_password_dialog import ChangePasswordDialog
from src.utils.app_translator import get_text
from src.utils.language_manager import get_language_manager, get_text as lang_get_text
from src.utils.theme_manager import get_theme_manager, ThemeMode
from datetime import datetime

class ModernMainWindow(QMainWindow):
    """Enhanced main window with responsive design and modern styling."""
    
    def __init__(self, db_manager, username):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
        
        # Initialize managers
        self.language_manager = get_language_manager()
        self.theme_manager = get_theme_manager()
        self.style_manager = get_style_manager()
        
        # Register callbacks
        self.language_manager.register_language_change_callback(self.on_language_updated)
        self.theme_manager.register_theme_change_callback(self.on_theme_updated)
        self.style_manager.style_changed.connect(self.apply_styles)
        
        # Current layout mode
        self.current_size_class = "md"
        
        # Initialize UI
        self.init_ui()
        self.load_persons()
        self.apply_styles()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_persons)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def init_ui(self):
        """Initialize the user interface with responsive design."""
        self.setWindowTitle(f"Psychological Records System - {self.username}")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)
        
        # Create central widget with responsive container
        self.central_widget = ResponsiveMainWidget(self.db_manager, self.username)
        self.setCentralWidget(self.central_widget)
        
        # Connect signals
        self.central_widget.person_selected.connect(self.on_person_selected)
        self.central_widget.person_added.connect(self.on_person_added)
        self.central_widget.person_edited.connect(self.on_person_edited)
        self.central_widget.person_deleted.connect(self.on_person_deleted)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.create_status_bar()
        
        # Create toolbar
        self.create_toolbar()
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(self.get_text('main_window.file'))
        
        new_person_action = QAction(self.get_text('main_window.new_person'), self)
        new_person_action.setShortcut('Ctrl+N')
        new_person_action.triggered.connect(self.central_widget.add_person)
        file_menu.addAction(new_person_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(self.get_text('main_window.exit'), self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu(self.get_text('main_window.view'))
        
        refresh_action = QAction(self.get_text('main_window.refresh'), self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.load_persons)
        view_menu.addAction(refresh_action)
        
        view_menu.addSeparator()
        
        toggle_theme_action = QAction(self.get_text('main_window.toggle_theme'), self)
        toggle_theme_action.setShortcut('Ctrl+T')
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu(self.get_text('main_window.help'))
        
        about_action = QAction(self.get_text('main_window.about'), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create the application toolbar."""
        toolbar = self.addToolBar('Main')
        toolbar.setMovable(False)
        
        # Add person
        add_action = QAction('➕ ' + self.get_text('main_window.add_person'), self)
        add_action.triggered.connect(self.central_widget.add_person)
        toolbar.addAction(add_action)
        
        toolbar.addSeparator()
        
        # Refresh
        refresh_action = QAction('🔄 ' + self.get_text('main_window.refresh'), self)
        refresh_action.triggered.connect(self.load_persons)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # Theme toggle
        self.theme_action = QAction('🌙', self)
        self.theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(self.theme_action)
        
        # Add stretch
        spacer = QWidget()
        spacer.setSizePolicy(QWidget.SizePolicy.Policy.Expanding, QWidget.SizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)
        
        # User info
        user_label = QLabel(f"👤 {self.username}")
        user_label.setProperty("class", "caption")
        toolbar.addWidget(user_label)
    
    def create_status_bar(self):
        """Create the application status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.get_text('main_window.ready'))
    
    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize events."""
        super().resizeEvent(event)
        
        # Update style manager with new size
        self.style_manager.update_size_class(event.size().width(), event.size().height())
        
        # Update current size class
        new_size_class = ResponsiveBreakpoints.get_size_class(event.size().width())
        if new_size_class != self.current_size_class:
            self.current_size_class = new_size_class
            self.adapt_to_size_class(new_size_class)
    
    def adapt_to_size_class(self, size_class):
        """Adapt UI elements to new size class."""
        if hasattr(self.central_widget, 'adapt_to_size_class'):
            self.central_widget.adapt_to_size_class(size_class)
    
    def apply_styles(self):
        """Apply the current stylesheet."""
        stylesheet = self.style_manager.get_current_stylesheet()
        self.setStyleSheet(stylesheet)
        
        # Update theme toggle icon
        current_theme = self.theme_manager.get_current_theme()
        if hasattr(self, 'theme_action'):
            self.theme_action.setText('☀️' if current_theme == ThemeMode.DARK else '🌙')
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        current_theme = self.theme_manager.get_current_theme()
        new_theme = ThemeMode.DARK if current_theme == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.theme_manager.change_theme(new_theme)
    
    def load_persons(self):
        """Load persons from database."""
        if hasattr(self.central_widget, 'load_persons'):
            self.central_widget.load_persons()
        self.status_bar.showMessage(f"{self.get_text('main_window.last_updated')}: {datetime.now().strftime('%H:%M:%S')}")
    
    def on_person_selected(self, person_data):
        """Handle person selection."""
        self.status_bar.showMessage(f"{self.get_text('main_window.selected')}: {person_data[1]}")
    
    def on_person_added(self, person_data):
        """Handle person addition."""
        self.status_bar.showMessage(f"{self.get_text('main_window.added')}: {person_data[1]}")
        self.load_persons()
    
    def on_person_edited(self, person_data):
        """Handle person editing."""
        self.status_bar.showMessage(f"{self.get_text('main_window.updated')}: {person_data[1]}")
        self.load_persons()
    
    def on_person_deleted(self, person_data):
        """Handle person deletion."""
        self.status_bar.showMessage(f"{self.get_text('main_window.deleted')}: {person_data[1]}")
        self.load_persons()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, self.get_text('main_window.about'), 
                         f"{self.get_text('main_window.about_text')}\\n\\nVersion 2.0")
    
    def on_language_updated(self, locale: str):
        """Handle language updates."""
        # Update menu bar
        self.menuBar().clear()
        self.create_menu_bar()
        
        # Update toolbar
        self.removeToolBar(self.toolBar())
        self.create_toolbar()
        
        # Update central widget
        if hasattr(self.central_widget, 'on_language_updated'):
            self.central_widget.on_language_updated(locale)
    
    def on_theme_updated(self, theme_mode: ThemeMode):
        """Handle theme updates."""
        self.apply_styles()
        if hasattr(self.central_widget, 'on_theme_updated'):
            self.central_widget.on_theme_updated(theme_mode)
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)

class ResponsiveMainWidget(ResponsiveWidget):
    """Main widget with responsive layout for person management."""
    
    person_selected = pyqtSignal(tuple)
    person_added = pyqtSignal(tuple)
    person_edited = pyqtSignal(tuple)
    person_deleted = pyqtSignal(tuple)
    
    def __init__(self, db_manager, username):
        super().__init__()
        self.db_manager = db_manager
        self.username = username
        self.current_layout_mode = "standard"
        
        self.init_ui()
        self.layout_mode_changed.connect(self.on_layout_mode_changed)
    
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)
        
        # Create header
        self.create_header()
        
        # Create content area
        self.create_content_area()
        
        # Create action buttons
        self.create_action_buttons()
    
    def create_header(self):
        """Create the header section."""
        # Title
        self.title_label = QLabel(self.get_text('main_window.title'))
        self.title_label.setProperty("class", "title")
        
        # Search section
        self.search_container = QWidget()
        search_layout = QHBoxLayout(self.search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        search_label = QLabel(f"🔍 {self.get_text('main_window.search')}:")
        search_label.setProperty("class", "caption")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.get_text('main_window.search_placeholder'))
        self.search_input.textChanged.connect(self.filter_persons)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        
        # User info
        self.user_info = QLabel(f"👤 {self.get_text('main_window.logged_in_as')}: {self.username}")
        self.user_info.setProperty("class", "subtitle")
        
        # Create responsive header
        self.header_frame = FlexibleLayout.create_header_layout(
            self.title_label, 
            [self.search_container, self.user_info],
            responsive=True
        )
        
        self.main_layout.addWidget(self.header_frame)
    
    def create_content_area(self):
        """Create the main content area with table."""
        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setProperty("class", "card")
        content_layout = QVBoxLayout(self.content_frame)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        
        content_layout.addWidget(self.table)
        self.main_layout.addWidget(self.content_frame)
    
    def setup_table(self):
        """Setup the persons table."""
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            self.get_text('main_window.id'),
            self.get_text('main_window.name'),
            self.get_text('main_window.cnp'),
            self.get_text('main_window.created')
        ])
        
        # Hide ID column
        self.table.setColumnHidden(0, True)
        
        # Configure header
        header = self.table.horizontalHeader()
        header.setVisible(True)
        header.setMinimumHeight(40)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Table properties
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.edit_person)
    
    def create_action_buttons(self):
        """Create action buttons with responsive layout."""
        # Button definitions
        self.add_button = QPushButton(f"➕ {self.get_text('main_window.add_person')}")
        self.add_button.setProperty("class", "success")
        self.add_button.clicked.connect(self.add_person)
        
        self.edit_button = QPushButton(f"✏️ {self.get_text('main_window.edit_person')}")
        self.edit_button.clicked.connect(self.edit_person)
        self.edit_button.setEnabled(False)
        
        self.delete_button = QPushButton(f"🗑️ {self.get_text('main_window.delete_person')}")
        self.delete_button.setProperty("class", "danger")
        self.delete_button.clicked.connect(self.delete_person)
        self.delete_button.setEnabled(False)
        
        self.medical_records_button = QPushButton(f"📋 {self.get_text('main_window.medical_records')}")
        self.medical_records_button.clicked.connect(self.view_medical_records)
        self.medical_records_button.setEnabled(False)
        
        self.refresh_button = QPushButton(f"🔄 {self.get_text('main_window.refresh')}")
        self.refresh_button.setProperty("class", "secondary")
        self.refresh_button.clicked.connect(self.load_persons)
        
        # Create responsive button group
        buttons = [self.add_button, self.edit_button, self.delete_button, 
                  self.medical_records_button, self.refresh_button]
        
        self.button_container = FlexibleLayout.create_button_group(buttons, responsive=True)
        self.main_layout.addWidget(self.button_container)
    
    def adapt_to_layout_mode(self, mode):
        """Adapt layout to different screen sizes."""
        if mode == "xs" or mode == "sm":
            # Mobile layout: stack buttons vertically
            self.adapt_to_mobile_layout()
        else:
            # Desktop layout: buttons horizontally
            self.adapt_to_desktop_layout()
    
    def adapt_to_mobile_layout(self):
        """Adapt to mobile layout."""
        # Update button container for vertical layout
        if hasattr(self, 'button_container') and self.button_container.layout():
            layout = self.button_container.layout()
            
            # Clear and recreate with vertical layout
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                if item.widget():
                    item.widget().setParent(None)
            
            # Recreate with vertical layout
            buttons = [self.add_button, self.edit_button, self.delete_button, 
                      self.medical_records_button, self.refresh_button]
            
            new_layout = QVBoxLayout(self.button_container)
            for button in buttons:
                new_layout.addWidget(button)
    
    def adapt_to_desktop_layout(self):
        """Adapt to desktop layout."""
        # Update button container for horizontal layout
        if hasattr(self, 'button_container') and self.button_container.layout():
            layout = self.button_container.layout()
            
            # Clear and recreate with horizontal layout
            for i in reversed(range(layout.count())):
                item = layout.takeAt(i)
                if item.widget():
                    item.widget().setParent(None)
            
            # Recreate with horizontal layout
            buttons = [self.add_button, self.edit_button, self.delete_button, 
                      self.medical_records_button, self.refresh_button]
            
            new_layout = QHBoxLayout(self.button_container)
            for button in buttons:
                new_layout.addWidget(button)
            new_layout.addStretch()
    
    def load_persons(self):
        """Load persons from database."""
        try:
            persons = self.db_manager.get_all_persons()
            self.table.setRowCount(len(persons))
            
            for row, person in enumerate(persons):
                self.table.setItem(row, 0, QTableWidgetItem(str(person[0])))  # ID
                self.table.setItem(row, 1, QTableWidgetItem(person[1]))       # Name
                self.table.setItem(row, 2, QTableWidgetItem(person[2]))       # CNP
                self.table.setItem(row, 3, QTableWidgetItem(person[3][:10]))  # Created date
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load persons: {str(e)}")
    
    def filter_persons(self, text):
        """Filter persons based on search text."""
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            cnp_item = self.table.item(row, 2)
            
            if name_item and cnp_item:
                match = (text.lower() in name_item.text().lower() or 
                        text.lower() in cnp_item.text().lower())
                self.table.setRowHidden(row, not match)
    
    def on_selection_changed(self):
        """Handle table selection changes."""
        selected = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(selected)
        self.delete_button.setEnabled(selected)
        self.medical_records_button.setEnabled(selected)
        
        if selected:
            person_data = self.get_selected_person()
            if person_data:
                self.person_selected.emit(person_data)
    
    def get_selected_person(self):
        """Get currently selected person data."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            return (
                int(self.table.item(current_row, 0).text()),  # ID
                self.table.item(current_row, 1).text(),       # Name
                self.table.item(current_row, 2).text(),       # CNP
                self.table.item(current_row, 3).text()        # Created
            )
        return None
    
    def add_person(self):
        """Add a new person."""
        dialog = PersonDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            person_data = dialog.get_person_data()
            if person_data:
                success = self.db_manager.add_person(person_data['name'], person_data['cnp'])
                if success:
                    self.person_added.emit((0, person_data['name'], person_data['cnp'], ''))
                else:
                    QMessageBox.critical(self, "Error", "Failed to add person.")
    
    def edit_person(self):
        """Edit selected person."""
        person_data = self.get_selected_person()
        if person_data:
            dialog = PersonDialog(person_data, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_person_data()
                if new_data:
                    success = self.db_manager.update_person(person_data[0], new_data['name'], new_data['cnp'])
                    if success:
                        self.person_edited.emit((person_data[0], new_data['name'], new_data['cnp'], person_data[3]))
                    else:
                        QMessageBox.critical(self, "Error", "Failed to update person.")
    
    def delete_person(self):
        """Delete selected person."""
        person_data = self.get_selected_person()
        if person_data:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete {person_data[1]}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.db_manager.delete_person(person_data[0])
                if success:
                    self.person_deleted.emit(person_data)
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete person.")
    
    def view_medical_records(self):
        """View medical records for selected person."""
        person_data = self.get_selected_person()
        if person_data:
            from src.ui.medical_records_window import MedicalRecordsWindow
            self.medical_window = MedicalRecordsWindow(person_data, self.db_manager, self)
            self.medical_window.show()
    
    def on_layout_mode_changed(self, mode):
        """Handle layout mode changes."""
        self.current_layout_mode = mode.value
        # Additional responsive adaptations can be added here
    
    def on_language_updated(self, locale: str):
        """Handle language updates."""
        # Update all text elements
        self.title_label.setText(self.get_text('main_window.title'))
        # Update other UI elements...
    
    def on_theme_updated(self, theme_mode):
        """Handle theme updates."""
        # Additional theme-specific adaptations can be added here
        pass
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)
