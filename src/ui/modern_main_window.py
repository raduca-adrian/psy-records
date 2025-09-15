"""
Enhanced Main Window with responsive design and modern QSS styling.
"""

import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QLabel, QHeaderView, QMenuBar, 
                            QMenu, QStatusBar, QToolBar, QLineEdit, QDialog,
                            QFrame, QSplitter, QScrollArea, QGridLayout,
                            QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QFont, QResizeEvent

from .responsive_layout import (
    ResponsiveWidget,
    ResponsiveBreakpoints,
)
from .modern_qss import get_style_manager
from .person_dialog import PersonDialog
from .change_password_dialog import ChangePasswordDialog
from ..utils.app_translator import get_text
from ..utils.language_manager import get_language_manager, get_text as lang_get_text
from ..utils.theme_manager import get_theme_manager, ThemeMode
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
        # Keep a reference so we can remove/recreate it safely on language change
        self.toolbar = self.addToolBar('Main')
        self.toolbar.setMovable(False)

        # Add person
        add_action = QAction('➕ ' + self.get_text('main_window.add_person'), self)
        add_action.triggered.connect(self.central_widget.add_person)
        self.toolbar.addAction(add_action)

        self.toolbar.addSeparator()

        # Refresh
        refresh_action = QAction('🔄 ' + self.get_text('main_window.refresh'), self)
        refresh_action.triggered.connect(self.load_persons)
        self.toolbar.addAction(refresh_action)

        self.toolbar.addSeparator()

        # Theme toggle
        self.theme_action = QAction('🌙', self)
        self.theme_action.triggered.connect(self.toggle_theme)
        self.toolbar.addAction(self.theme_action)

        # Add stretch
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)

        # User info
        user_label = QLabel(f"👤 {self.username}")
        user_label.setProperty("class", "caption")
        self.toolbar.addWidget(user_label)
    
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
        if hasattr(self, 'toolbar') and self.toolbar is not None:
            try:
                self.removeToolBar(self.toolbar)
            except Exception:
                pass
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
        """Initialize the user interface with a simple, readable layout."""
        # Main vertical layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)

        # Create main content sections
        self.create_header_section()
        self.create_search_section()
        self.create_content_section()
        self.create_actions_section()
    
    def create_header_section(self):
        """Create the header section with title and user info."""
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        
        # Title
        self.title_label = QLabel(self.get_text('main_window.title'))
        self.title_label.setProperty("class", "title")
        header_layout.addWidget(self.title_label)
        
        # User info
        self.user_label = QLabel(f"{self.get_text('main_window.logged_in_as')}: {self.username}")
        self.user_label.setProperty("class", "subtitle")
        header_layout.addWidget(self.user_label)
        
        # Add to main layout
        self.main_layout.addWidget(header_container)
    
    def create_search_section(self):
        """Create the search and filter section."""
        search_container = QWidget()
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(8)
        
        # Search label
        search_label = QLabel(self.get_text('main_window.search'))
        search_label.setProperty("class", "label")
        search_layout.addWidget(search_label)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.get_text('main_window.search_placeholder'))
        # Connect to filtering routine
        self.search_input.textChanged.connect(self.filter_persons)
        self.search_input.setProperty("class", "search")
        search_layout.addWidget(self.search_input)
        
        # Add to main layout
        self.main_layout.addWidget(search_container)
    
    def create_content_section(self):
        """Create the main content table section."""
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        content_layout.addWidget(self.table)
        
        # Add to main layout - table takes most space
        self.main_layout.addWidget(content_container, 1)
    
    def create_actions_section(self):
        """Create the action buttons section."""
        actions_container = QWidget()
        self.actions_layout = QHBoxLayout(actions_container)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(8)

        # Create action buttons
        self.create_action_buttons()

        # Add stretch at the end for spacing
        self.actions_layout.addStretch()

        # Add to main layout
        self.main_layout.addWidget(actions_container)
    
    def create_action_buttons(self):
        """Create action buttons with proper grid alignment."""
        # Add Person button
        self.add_person_btn = QPushButton(f"👤 {self.get_text('main_window.add_person')}")
        self.add_person_btn.setProperty("class", "success")
        self.add_person_btn.clicked.connect(self.add_person)
        self.actions_layout.addWidget(self.add_person_btn)
        
        # Edit Person button
        self.edit_person_btn = QPushButton(f"✏️ {self.get_text('main_window.edit_person')}")
        self.edit_person_btn.clicked.connect(self.edit_person)
        self.edit_person_btn.setEnabled(False)
        self.actions_layout.addWidget(self.edit_person_btn)
        
        # Delete Person button
        self.delete_person_btn = QPushButton(f"🗑️ {self.get_text('main_window.delete_person')}")
        self.delete_person_btn.setProperty("class", "danger")
        self.delete_person_btn.clicked.connect(self.delete_person)
        self.delete_person_btn.setEnabled(False)
        self.actions_layout.addWidget(self.delete_person_btn)
        
        # View Records button
        self.view_records_btn = QPushButton(f"📋 {self.get_text('main_window.view_records')}")
        self.view_records_btn.setProperty("class", "primary")
        self.view_records_btn.clicked.connect(self.view_medical_records)
        self.view_records_btn.setEnabled(False)
        self.actions_layout.addWidget(self.view_records_btn)
        
        # Theme Toggle button
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setProperty("class", "icon")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.update_theme_button()
        self.actions_layout.addWidget(self.theme_toggle_btn)
    
    # (grid layout removed)
    
    # (removed duplicate older setup_table implementation)
    
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
    
    # (removed legacy create_action_buttons without parameters to avoid signature conflict)
    
    def adapt_to_layout_mode(self, mode):
        """No-op: grid system removed; keep method for compatibility."""
        pass
    
    def adapt_to_mobile_layout(self):
        """Removed: not used without grid system."""
        pass
    
    def adapt_to_desktop_layout(self):
        """Removed: not used without grid system."""
        pass
    
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
        # Enable/disable actions created in container-based button setup
        if hasattr(self, 'edit_person_btn'):
            self.edit_person_btn.setEnabled(selected)
        if hasattr(self, 'delete_person_btn'):
            self.delete_person_btn.setEnabled(selected)
        if hasattr(self, 'view_records_btn'):
            self.view_records_btn.setEnabled(selected)
        
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
        dialog = PersonDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            person_data = dialog.get_person_data()
            if person_data:
                success = self.db_manager.add_person(person_data['name'], person_data['cnp'])
                if success:
                    self.person_added.emit((0, person_data['name'], person_data['cnp'], ''))
                else:
                    QMessageBox.critical(self, "Error", "Failed to add person. CNP might already exist.")
    
    def edit_person(self):
        """Edit selected person."""
        person_data = self.get_selected_person()
        if person_data:
            dialog = PersonDialog(self.db_manager, person_data, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_person_data()
                if new_data:
                    success = self.db_manager.update_person(person_data[0], new_data['name'], new_data['cnp'])
                    if success:
                        self.person_edited.emit((person_data[0], new_data['name'], new_data['cnp'], person_data[3]))
                    else:
                        QMessageBox.critical(self, "Error", "Failed to update person. CNP might already exist.")
    
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
            from .modern_medical_records_window import ModernMedicalRecordsWindow
            self.medical_window = ModernMedicalRecordsWindow(person_data, self.db_manager, self)
            self.medical_window.show()
    
    def on_layout_mode_changed(self, mode):
        """Handle layout mode changes."""
        self.current_layout_mode = mode.value
        # Additional responsive adaptations can be added here
    
    def on_language_updated(self, locale: str):
        """Handle language updates."""
        # Update localized UI elements within this widget
        try:
            self.title_label.setText(self.get_text('main_window.title'))
        except Exception:
            pass
        # Update table headers
        try:
            self.table.setHorizontalHeaderLabels([
                self.get_text('main_window.id'),
                self.get_text('main_window.name'),
                self.get_text('main_window.cnp'),
                self.get_text('main_window.created')
            ])
        except Exception:
            pass
        # Update action buttons
        try:
            self.add_person_btn.setText(f"👤 {self.get_text('main_window.add_person')}")
            self.edit_person_btn.setText(f"✏️ {self.get_text('main_window.edit_person')}")
            self.delete_person_btn.setText(f"🗑️ {self.get_text('main_window.delete_person')}")
            self.view_records_btn.setText(f"📋 {self.get_text('main_window.view_records')}")
        except Exception:
            pass
    
    def on_theme_updated(self, theme_mode):
        """Handle theme updates."""
        # Additional theme-specific adaptations can be added here
        pass
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)

    # --- Theme helpers for actions grid ---
    def update_theme_button(self):
        """Update theme toggle button icon/text based on current theme."""
        if hasattr(self, 'theme_toggle_btn'):
            current_theme = get_theme_manager().get_current_theme()
            self.theme_toggle_btn.setText('☀️' if current_theme == ThemeMode.DARK else '🌙')

    def toggle_theme(self):
        """Delegate theme toggle to main window/theme manager if available."""
        tm = get_theme_manager()
        current = tm.get_current_theme()
        tm.change_theme(ThemeMode.DARK if current == ThemeMode.LIGHT else ThemeMode.LIGHT)
