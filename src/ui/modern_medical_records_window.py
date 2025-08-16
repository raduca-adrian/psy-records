"""
Enhanced Medical Records Window with responsive design and modern QSS styling.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QTabWidget, QMessageBox, QHeaderView, QFileDialog,
                            QFrame, QSplitter, QTextEdit, QScrollArea, QDialog,
                            QGridLayout)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QResizeEvent

from src.ui.responsive_layout import (ResponsiveWidget, FlexibleLayout, 
                                    ResponsiveBreakpoints, LayoutUtils)
from src.ui.modern_qss import get_style_manager
from src.core.database import DatabaseManager
from src.ui.assessment_dialog import AssessmentDialog
from src.ui.consultation_dialog import ConsultationDialog
from src.utils.pdf_generator import generate_psychological_report
from src.utils.language_manager import get_language_manager, get_text as lang_get_text
from src.utils.theme_manager import get_theme_manager, ThemeMode

class ModernMedicalRecordsWindow(QMainWindow):
    """Enhanced medical records window with responsive design."""
    
    def __init__(self, person_data, db_manager, parent=None):
        super().__init__(parent)
        self.person_data = person_data
        self.db_manager = db_manager
        self.person_id = person_data[0]
        self.person_name = person_data[1]
        self.person_cnp = person_data[2]
        
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
        
        self.init_ui()
        self.load_medical_records()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(f"{self.get_text('psychological_records.title')} - {self.person_name}")
        self.setMinimumSize(900, 700)
        self.resize(1400, 900)
        
        # Create central widget
        self.central_widget = ResponsiveMedicalWidget(
            self.person_data, self.db_manager, self
        )
        self.setCentralWidget(self.central_widget)
        
        # Connect signals
        self.central_widget.records_updated.connect(self.load_medical_records)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(self.get_text('main_window.file'))
        
        new_assessment_action = file_menu.addAction(
            f"📋 {self.get_text('psychological_records.new_assessment')}"
        )
        new_assessment_action.triggered.connect(self.central_widget.add_assessment)
        
        new_consultation_action = file_menu.addAction(
            f"💬 {self.get_text('psychological_records.new_session')}"
        )
        new_consultation_action.triggered.connect(self.central_widget.add_consultation)
        
        file_menu.addSeparator()
        
        generate_report_action = file_menu.addAction(
            f"📄 {self.get_text('psychological_records.generate_report')}"
        )
        generate_report_action.triggered.connect(self.central_widget.generate_pdf_report)
        
        file_menu.addSeparator()
        
        close_action = file_menu.addAction(self.get_text('common.close'))
        close_action.triggered.connect(self.close)
        
        # View menu
        view_menu = menubar.addMenu(self.get_text('main_window.view'))
        
        refresh_action = view_menu.addAction(self.get_text('main_window.refresh'))
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.load_medical_records)
        
        view_menu.addSeparator()
        
        toggle_theme_action = view_menu.addAction(self.get_text('main_window.toggle_theme'))
        toggle_theme_action.setShortcut('Ctrl+T')
        toggle_theme_action.triggered.connect(self.toggle_theme)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage(f"{self.get_text('psychological_records.client')}: {self.person_name}")
    
    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize events."""
        super().resizeEvent(event)
        
        # Update style manager with new size
        self.style_manager.update_size_class(event.size().width(), event.size().height())
        
        # Update current size class
        new_size_class = ResponsiveBreakpoints.get_size_class(event.size().width())
        if new_size_class != self.current_size_class:
            self.current_size_class = new_size_class
            if hasattr(self.central_widget, 'adapt_to_size_class'):
                self.central_widget.adapt_to_size_class(new_size_class)
    
    def apply_styles(self):
        """Apply the current stylesheet."""
        stylesheet = self.style_manager.get_current_stylesheet()
        self.setStyleSheet(stylesheet)
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        current_theme = self.theme_manager.get_current_theme()
        new_theme = ThemeMode.DARK if current_theme == ThemeMode.LIGHT else ThemeMode.LIGHT
        self.theme_manager.change_theme(new_theme)
    
    def load_medical_records(self):
        """Load medical records."""
        if hasattr(self.central_widget, 'load_medical_records'):
            self.central_widget.load_medical_records()
    
    def on_language_updated(self, locale: str):
        """Handle language updates."""
        self.setWindowTitle(f"{self.get_text('psychological_records.title')} - {self.person_name}")
        # Update menu bar
        self.menuBar().clear()
        self.create_menu_bar()
        
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
    
    def closeEvent(self, event):
        """Clean up when window is closed."""
        # Unregister callbacks
        if hasattr(self, 'language_manager'):
            self.language_manager.unregister_language_change_callback(self.on_language_updated)
        if hasattr(self, 'theme_manager'):
            self.theme_manager.unregister_theme_change_callback(self.on_theme_updated)
        super().closeEvent(event)

class ResponsiveMedicalWidget(ResponsiveWidget):
    """Medical records widget with responsive layout."""
    
    records_updated = pyqtSignal()
    
    def __init__(self, person_data, db_manager, parent=None):
        super().__init__(parent)
        self.person_data = person_data
        self.db_manager = db_manager
        self.person_id = person_data[0]
        self.person_name = person_data[1]
        self.person_cnp = person_data[2]
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
    
    def create_header(self):
        """Create the header section."""
        # Title and patient info
        self.title_label = QLabel(f"{self.get_text('psychological_records.title')} - {self.person_name}")
        self.title_label.setProperty("class", "title")
        
        self.info_label = QLabel(f"CNP: {self.person_cnp} | {self.get_text('psychological_records.client_id')}: {self.person_id}")
        self.info_label.setProperty("class", "subtitle")
        
        # Action buttons
        self.add_assessment_btn = QPushButton(f"📋 {self.get_text('psychological_records.new_assessment')}")
        self.add_assessment_btn.setProperty("class", "success")
        self.add_assessment_btn.clicked.connect(self.add_assessment)
        
        self.add_consultation_btn = QPushButton(f"💬 {self.get_text('psychological_records.new_session')}")
        self.add_consultation_btn.clicked.connect(self.add_consultation)
        
        self.generate_report_btn = QPushButton(f"📄 {self.get_text('psychological_records.generate_report')}")
        self.generate_report_btn.setProperty("class", "warning")
        self.generate_report_btn.clicked.connect(self.generate_pdf_report)
        
        self.refresh_btn = QPushButton(f"🔄 {self.get_text('main_window.refresh')}")
        self.refresh_btn.setProperty("class", "secondary")
        self.refresh_btn.clicked.connect(self.load_medical_records)
        
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setProperty("class", "icon")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.update_theme_button()
        
        # Create responsive header layout
        action_buttons = [
            self.add_assessment_btn, self.add_consultation_btn,
            self.generate_report_btn, self.refresh_btn, self.theme_toggle_btn
        ]
        
        # Header container
        header_container = QWidget()
        header_layout = QVBoxLayout(header_container)
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.info_label)
        
        # Button container
        self.button_container = FlexibleLayout.create_button_group(
            action_buttons, responsive=True
        )
        header_layout.addWidget(self.button_container)
        
        self.main_layout.addWidget(header_container)
    
    def create_content_area(self):
        """Create the main content area with tabs."""
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Assessments tab
        self.assessments_tab = ResponsiveAssessmentsTab(self.person_id, self.db_manager)
        self.assessments_tab.records_updated.connect(self.records_updated.emit)
        self.tab_widget.addTab(
            self.assessments_tab, 
            f"📋 {self.get_text('psychological_records.assessments_tab')}"
        )
        
        # Consultations tab
        self.consultations_tab = ResponsiveConsultationsTab(self.person_id, self.db_manager)
        self.consultations_tab.records_updated.connect(self.records_updated.emit)
        self.tab_widget.addTab(
            self.consultations_tab,
            f"💬 {self.get_text('psychological_records.sessions_tab')}"
        )
        
        self.main_layout.addWidget(self.tab_widget)
    
    def adapt_to_layout_mode(self, mode):
        """Adapt layout to different screen sizes."""
        size_class = ResponsiveBreakpoints.get_size_class(self.width())
        
        if size_class in ["xs", "sm"]:
            # Mobile layout adaptations
            self.adapt_to_mobile_layout()
        else:
            # Desktop layout adaptations
            self.adapt_to_desktop_layout()
    
    def adapt_to_mobile_layout(self):
        """Adapt to mobile layout."""
        # Make tabs scrollable on mobile
        self.tab_widget.setElideMode(Qt.TextElideMode.ElideRight)
        
        # Adjust button layout for mobile
        if hasattr(self, 'button_container') and self.button_container.layout():
            layout = self.button_container.layout()
            if isinstance(layout, QHBoxLayout):
                # Convert to vertical layout for mobile
                self.recreate_button_layout(vertical=True)
    
    def adapt_to_desktop_layout(self):
        """Adapt to desktop layout."""
        # Reset tab elide mode
        self.tab_widget.setElideMode(Qt.TextElideMode.ElideNone)
        
        # Adjust button layout for desktop
        if hasattr(self, 'button_container') and self.button_container.layout():
            layout = self.button_container.layout()
            if isinstance(layout, QVBoxLayout):
                # Convert to horizontal layout for desktop
                self.recreate_button_layout(vertical=False)
    
    def recreate_button_layout(self, vertical=False):
        """Recreate button layout with specified orientation."""
        if not hasattr(self, 'button_container'):
            return
            
        # Get buttons
        buttons = [
            self.add_assessment_btn, self.add_consultation_btn,
            self.generate_report_btn, self.refresh_btn, self.theme_toggle_btn
        ]
        
        # Clear existing layout
        old_layout = self.button_container.layout()
        if old_layout:
            for i in reversed(range(old_layout.count())):
                item = old_layout.takeAt(i)
                if item.widget():
                    item.widget().setParent(None)
        
        # Create new layout
        if vertical:
            new_layout = QVBoxLayout(self.button_container)
        else:
            new_layout = QHBoxLayout(self.button_container)
        
        # Add buttons
        for button in buttons:
            new_layout.addWidget(button)
        
        if not vertical:
            new_layout.addStretch()
    
    def load_medical_records(self):
        """Load medical records from database."""
        self.assessments_tab.load_assessments()
        self.consultations_tab.load_consultations()
    
    def add_assessment(self):
        """Add a new assessment."""
        self.assessments_tab.add_assessment()
    
    def add_consultation(self):
        """Add a new consultation."""
        self.consultations_tab.add_consultation()
    
    def generate_pdf_report(self):
        """Generate a PDF medical report."""
        try:
            # Get complete psychological record
            record = self.db_manager.get_person_complete_record(self.person_id)
            
            if not record:
                QMessageBox.warning(self, "No Data", "No psychological records found for this client.")
                return
            
            # Ask user for save location
            filename = f"Psychological_Report_{self.person_name.replace(' ', '_')}_{QDate.currentDate().toString('yyyy-MM-dd')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Psychological Report", 
                filename,
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Generate the report
            success = generate_psychological_report(
                record['person'],
                record['assessments'],
                record['consultations'],
                file_path
            )
            
            if success:
                QMessageBox.information(self, "Success", 
                                      f"Psychological report generated successfully!\\n\\nSaved to: {file_path}")
                
                # Ask if user wants to open the file
                reply = QMessageBox.question(self, "Open Report", 
                                           "Would you like to open the report now?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    import os
                    os.startfile(file_path)  # Windows
            else:
                QMessageBox.critical(self, "Error", "Failed to generate psychological report.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the report:\\n{str(e)}")
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        theme_manager = get_theme_manager()
        current_theme = theme_manager.get_current_theme()
        new_theme = ThemeMode.DARK if current_theme == ThemeMode.LIGHT else ThemeMode.LIGHT
        theme_manager.change_theme(new_theme)
    
    def update_theme_button(self):
        """Update theme toggle button icon."""
        theme_manager = get_theme_manager()
        current_theme = theme_manager.get_current_theme()
        self.theme_toggle_btn.setText('☀️' if current_theme == ThemeMode.DARK else '🌙')
    
    def on_layout_mode_changed(self, mode):
        """Handle layout mode changes."""
        self.current_layout_mode = mode.value
    
    def on_language_updated(self, locale: str):
        """Handle language updates."""
        # Update header elements
        self.title_label.setText(f"{self.get_text('psychological_records.title')} - {self.person_name}")
        self.info_label.setText(f"CNP: {self.person_cnp} | {self.get_text('psychological_records.client_id')}: {self.person_id}")
        
        # Update buttons
        self.add_assessment_btn.setText(f"📋 {self.get_text('psychological_records.new_assessment')}")
        self.add_consultation_btn.setText(f"💬 {self.get_text('psychological_records.new_session')}")
        self.generate_report_btn.setText(f"📄 {self.get_text('psychological_records.generate_report')}")
        self.refresh_btn.setText(f"🔄 {self.get_text('main_window.refresh')}")
        
        # Update tab titles
        self.tab_widget.setTabText(0, f"📋 {self.get_text('psychological_records.assessments_tab')}")
        self.tab_widget.setTabText(1, f"💬 {self.get_text('psychological_records.sessions_tab')}")
        
        # Update tabs
        if hasattr(self.assessments_tab, 'on_language_updated'):
            self.assessments_tab.on_language_updated(locale)
        if hasattr(self.consultations_tab, 'on_language_updated'):
            self.consultations_tab.on_language_updated(locale)
    
    def on_theme_updated(self, theme_mode: ThemeMode):
        """Handle theme updates."""
        self.update_theme_button()
        # Additional theme-specific adaptations can be added here
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)

class ResponsiveAssessmentsTab(ResponsiveWidget):
    """Responsive assessments tab."""
    
    records_updated = pyqtSignal()
    
    def __init__(self, person_id, db_manager):
        super().__init__()
        self.person_id = person_id
        self.db_manager = db_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Table
        self.assessments_table = QTableWidget()
        self.setup_table()
        
        # Make table scrollable on mobile
        scroll_area = FlexibleLayout.make_scrollable(self.assessments_table)
        layout.addWidget(scroll_area)
    
    def setup_table(self):
        """Setup the assessments table."""
        self.assessments_table.setColumnCount(6)
        self.assessments_table.setHorizontalHeaderLabels([
            self.get_text("psychological_records.date"), 
            self.get_text("psychological_records.presenting_problem"), 
            self.get_text("assessment.clinical_impressions"), 
            self.get_text("assessment.treatment_goals"), 
            self.get_text("main_window.created"), 
            self.get_text("psychological_records.actions")
        ])
        
        # Configure header
        header = self.assessments_table.horizontalHeader()
        header.setVisible(True)
        header.setMinimumHeight(40)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(5, 180)
        
        # Table properties
        self.assessments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.assessments_table.setAlternatingRowColors(True)
        self.assessments_table.verticalHeader().setDefaultSectionSize(50)
        self.assessments_table.verticalHeader().setVisible(False)
    
    def adapt_to_layout_mode(self, mode):
        """Adapt to layout mode changes."""
        if mode.value in ["xs", "sm"]:
            # Hide some columns on mobile
            self.assessments_table.setColumnHidden(2, True)  # Clinical impressions
            self.assessments_table.setColumnHidden(3, True)  # Treatment goals
        else:
            # Show all columns on desktop
            self.assessments_table.setColumnHidden(2, False)
            self.assessments_table.setColumnHidden(3, False)
    
    def load_assessments(self):
        """Load assessments from database."""
        # Implementation would go here
        pass
    
    def add_assessment(self):
        """Add a new assessment."""
        # Implementation would go here
        pass
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)

class ResponsiveConsultationsTab(ResponsiveWidget):
    """Responsive consultations tab."""
    
    records_updated = pyqtSignal()
    
    def __init__(self, person_id, db_manager):
        super().__init__()
        self.person_id = person_id
        self.db_manager = db_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Table
        self.consultations_table = QTableWidget()
        self.setup_table()
        
        # Make table scrollable on mobile
        scroll_area = FlexibleLayout.make_scrollable(self.consultations_table)
        layout.addWidget(scroll_area)
    
    def setup_table(self):
        """Setup the consultations table."""
        self.consultations_table.setColumnCount(7)
        self.consultations_table.setHorizontalHeaderLabels([
            self.get_text("psychological_records.date"), 
            self.get_text("psychological_records.session_type"), 
            self.get_text("psychological_records.session_focus"), 
            self.get_text("session.clinical_observations"), 
            self.get_text("psychological_records.interventions"), 
            self.get_text("session.next_session"), 
            self.get_text("psychological_records.actions")
        ])
        
        # Configure header
        header = self.consultations_table.horizontalHeader()
        header.setVisible(True)
        header.setMinimumHeight(40)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(6, 180)
        
        # Table properties
        self.consultations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.consultations_table.setAlternatingRowColors(True)
        self.consultations_table.verticalHeader().setDefaultSectionSize(50)
        self.consultations_table.verticalHeader().setVisible(False)
    
    def adapt_to_layout_mode(self, mode):
        """Adapt to layout mode changes."""
        if mode.value in ["xs", "sm"]:
            # Hide some columns on mobile
            self.consultations_table.setColumnHidden(3, True)  # Clinical observations
            self.consultations_table.setColumnHidden(4, True)  # Interventions
        else:
            # Show all columns on desktop
            self.consultations_table.setColumnHidden(3, False)
            self.consultations_table.setColumnHidden(4, False)
    
    def load_consultations(self):
        """Load consultations from database."""
        # Implementation would go here
        pass
    
    def add_consultation(self):
        """Add a new consultation."""
        # Implementation would go here
        pass
    
    def get_text(self, key):
        """Get translated text."""
        return lang_get_text(key, key)
