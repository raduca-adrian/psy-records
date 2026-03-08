"""
Unified single-window application for Psychological Records.
All functionality is contained within tabs - no separate dialogs.
"""

import os
from typing import Literal
from PyQt6.QtCore import Qt, QDate, QSettings
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QSplitter,
    QTextEdit,
    QTabWidget,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QMessageBox,
    QListWidget,
    QScrollArea,
    QFrame,
    QSpinBox,
)

from ..utils.pdf_generator import generate_psychological_report, generate_medical_consultation_form
from ..utils.language_manager import get_language_manager, get_text as _t
from ..utils.material_theme import get_material_stylesheet, get_theme_toggle_button_style
from ..utils.material_elevation import apply_card_elevation
from ..utils.system_theme_detector import detect_system_theme
from .language_selector_dialog import LanguageSelectorDialog

# Constants
NO_PATIENT_SELECTED_TITLE = "No patient selected"
NO_PATIENT_TITLE = "No Patient"
SELECT_PATIENT_MSG = "Please select a patient first."


class UnifiedMainWindow(QMainWindow):
    """Single unified window containing all application functionality."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.language_manager = get_language_manager()
        self.setWindowTitle(_t('app.title', 'Psychological Records'))
        self.setMinimumSize(1200, 700)

        # Load theme preference (detect from OS if not set)
        self.settings = QSettings('PsychologicalRecords', 'UnifiedApp')
        default_theme = detect_system_theme()
        self.current_theme: Literal["light", "dark"] = self.settings.value('theme', default_theme)

        # Create central widget with tab layout
        central = QWidget(self)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create tab widget
        self.tabs = QTabWidget(central)
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        
        # Initialize state (before creating tabs)
        self._initialized = False
        self.current_patient_id = None
        
        # Create all tabs
        self._create_patients_tab()
        self._create_add_patient_tab()
        self._create_checkup_tab()
        self._create_session_tab()
        self._create_medical_form_tab()
        
        # Initially disable tabs that require patient selection
        self._update_tab_accessibility()
        
        main_layout.addWidget(self.tabs)
        self.setCentralWidget(central)

        # Status bar with theme toggle
        status = QStatusBar(self)
        status.showMessage(_t('main_window.ready', 'Ready'))
        
        # Add language switcher button to status bar
        self.language_btn = QPushButton(f"🌍 {self.language_manager.get_language_display_name(self.language_manager.get_current_language())}", self)
        self.language_btn.setObjectName("languageToggle")
        self.language_btn.clicked.connect(self.change_language)
        self.language_btn.setToolTip(_t('menu.change_language', 'Change Language'))
        status.addPermanentWidget(self.language_btn)
        
        # Add theme toggle button to status bar
        self.theme_toggle_btn = QPushButton("", self)
        self.theme_toggle_btn.setObjectName("themeToggle")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self._update_theme_button_text()
        status.addPermanentWidget(self.theme_toggle_btn)
        
        self.setStatusBar(status)
        
        # Set up keyboard shortcuts
        self._setup_shortcuts()
        
        # Apply Material Design theme
        self.apply_theme(self.current_theme)

    def _create_patients_tab(self) -> None:
        """Create the main patients list and viewer tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        title = QLabel(_t('main_window.psychological_records', 'Patients'), tab)
        title.setProperty("class", "h1")
        layout.addWidget(title)

        subtitle = QLabel(_t('main_window.about_text', 'Manage patient records'), tab)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Button row
        button_row = QHBoxLayout()
        refresh_btn = QPushButton(_t('menu.refresh', 'Refresh'), tab)
        refresh_btn.clicked.connect(self.refresh_patients)
        export_pdf_btn = QPushButton(_t('psychological_records.generate_report', 'Export PDF'), tab)
        export_pdf_btn.clicked.connect(self.export_pdf)
        
        button_row.addWidget(refresh_btn)
        button_row.addWidget(export_pdf_btn)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        # Main content: splitter with table and details
        splitter = QSplitter(tab)
        
        # Left: Patient table
        left_panel = QWidget(splitter)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget(0, 5, left_panel)
        self.table.setHorizontalHeaderLabels([
            _t('main_window.id', 'ID'),
            _t('main_window.name', 'Name'),
            _t('main_window.cnp', 'CNP'),
            _t('main_window.registered', 'Registered'),
            _t('main_window.records', 'Records'),
        ])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.load_records_for_selected)
        
        # Improve table appearance
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, header.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(2, header.ResizeMode.Stretch)  # CNP
        header.setSectionResizeMode(3, header.ResizeMode.Fixed)  # Registered
        header.setSectionResizeMode(4, header.ResizeMode.Fixed)  # Records
        self.table.setColumnWidth(0, 50)  # ID
        self.table.setColumnWidth(3, 110)  # Registered date
        self.table.setColumnWidth(4, 80)  # Records count
        
        left_layout.addWidget(self.table)
        
        # Right: Records viewer with action buttons
        right_panel = QWidget(splitter)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Patient info card
        self.patient_info_frame = QFrame(right_panel)
        self.patient_info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.patient_info_frame.setProperty("class", "elevated")
        patient_info_layout = QVBoxLayout(self.patient_info_frame)
        
        self.patient_name_label = QLabel(NO_PATIENT_SELECTED_TITLE, self.patient_info_frame)
        self.patient_name_label.setProperty("class", "h2")
        patient_info_layout.addWidget(self.patient_name_label)
        
        self.patient_details_label = QLabel("", self.patient_info_frame)
        self.patient_details_label.setProperty("class", "subtitle")
        patient_info_layout.addWidget(self.patient_details_label)
        
        right_layout.addWidget(self.patient_info_frame)
        
        # Action buttons for selected patient
        action_label = QLabel(_t('main_window.quick_actions', 'Quick Actions:'), right_panel)
        action_label.setProperty("class", "h3")
        right_layout.addWidget(action_label)
        
        action_buttons = QHBoxLayout()
        new_checkup_btn = QPushButton('➕ ' + _t('common.new_checkup', 'New Checkup'), right_panel)
        new_checkup_btn.clicked.connect(self.start_add_checkup)
        new_session_btn = QPushButton('➕ ' + _t('common.new_session', 'New Session'), right_panel)
        new_session_btn.clicked.connect(self.start_add_session)
        new_medical_form_btn = QPushButton('📝 ' + _t('medical_form.quick_button', 'Medical Form'), right_panel)
        new_medical_form_btn.clicked.connect(self.start_medical_form)
        edit_checkup_btn = QPushButton('✏️ ' + _t('common.edit_checkup', 'Edit Checkup'), right_panel)
        edit_checkup_btn.clicked.connect(self.start_edit_checkup)
        edit_session_btn = QPushButton('✏️ ' + _t('common.edit_session', 'Edit Session'), right_panel)
        edit_session_btn.clicked.connect(self.start_edit_session)
        
        action_buttons.addWidget(new_checkup_btn)
        action_buttons.addWidget(new_session_btn)
        action_buttons.addWidget(new_medical_form_btn)
        action_buttons.addWidget(edit_checkup_btn)
        action_buttons.addWidget(edit_session_btn)
        action_buttons.addStretch(1)
        right_layout.addLayout(action_buttons)
        
        # Records view: combined Patient, Checkups, Sessions, Medical Forms
        records_label = QLabel(_t('main_window.record_summary', 'Record summary (Patient, Checkups, Sessions, Medical Forms)'), right_panel)
        records_label.setProperty("class", "h3")
        records_label.setWordWrap(True)
        right_layout.addWidget(records_label)
        
        self.records_view = QTextEdit(right_panel)
        self.records_view.setReadOnly(True)
        right_layout.addWidget(self.records_view)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        
        layout.addWidget(splitter)
        
        self.tabs.addTab(tab, "📋 " + _t('tabs.patients', 'Patients'))

    def _create_add_patient_tab(self) -> None:
        """Create the add/edit patient tab."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel(_t('patient_form.title', 'Add New Patient'), tab)
        title.setProperty("class", "h1")
        layout.addWidget(title)

        # Form
        form_frame = QFrame(tab)
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        # Match other elevated cards for consistent light/dark theming
        form_frame.setProperty("class", "elevated")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(12)

        form_layout.addWidget(QLabel(_t('patient_form.name_label', 'Name *'), form_frame))
        self.patient_name_edit = QLineEdit(form_frame)
        self.patient_name_edit.setPlaceholderText(_t('patient_form.name_placeholder', 'Enter patient full name'))
        form_layout.addWidget(self.patient_name_edit)

        form_layout.addWidget(QLabel(_t('patient_form.cnp_label', 'CNP *'), form_frame))
        self.patient_cnp_edit = QLineEdit(form_frame)
        self.patient_cnp_edit.setPlaceholderText(_t('patient_form.cnp_placeholder', 'Enter CNP (Personal Numeric Code)'))
        self.patient_cnp_edit.setMaxLength(32)
        form_layout.addWidget(self.patient_cnp_edit)

        # Buttons
        button_row = QHBoxLayout()
        clear_btn = QPushButton(_t('common.clear', 'Clear'), form_frame)
        clear_btn.clicked.connect(self.clear_patient_form)
        save_btn = QPushButton(_t('common.add_patient', 'Add Patient'), form_frame)
        save_btn.clicked.connect(self.save_patient)
        save_btn.setProperty("class", "primary")
        
        button_row.addWidget(clear_btn)
        button_row.addWidget(save_btn)
        button_row.addStretch(1)
        form_layout.addLayout(button_row)
        
        # Store frame reference for elevation effects
        self.patient_form_frame = form_frame
        
        layout.addWidget(form_frame)
        layout.addStretch(1)

        self.tabs.addTab(scroll, "➕ " + _t('tabs.add_patient', 'Add Patient'))

    def _create_checkup_tab(self) -> None:
        """Create the add/edit checkup tab."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.checkup_title_label = QLabel(_t('checkup_form.title_add', 'Add New Checkup'), tab)
        self.checkup_title_label.setProperty("class", "h1")
        layout.addWidget(self.checkup_title_label)

        # Patient info display
        self.checkup_patient_label = QLabel(NO_PATIENT_SELECTED_TITLE, tab)
        self.checkup_patient_label.setWordWrap(True)
        layout.addWidget(self.checkup_patient_label)

        # Record selector (for edit mode)
        self.checkup_selector_frame = QFrame(tab)
        self.checkup_selector_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.checkup_selector_frame.setVisible(False)
        selector_layout = QVBoxLayout(self.checkup_selector_frame)
        selector_layout.addWidget(QLabel(_t('common.select_checkup_edit', 'Select Checkup to Edit'), self.checkup_selector_frame))
        self.checkup_selector_list = QListWidget(self.checkup_selector_frame)
        self.checkup_selector_list.itemClicked.connect(self.load_checkup_for_edit)
        selector_layout.addWidget(self.checkup_selector_list)
        layout.addWidget(self.checkup_selector_frame)

        # Form
        form_frame = QFrame(tab)
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(12)

        form_layout.addWidget(QLabel(_t('checkup_form.date_label', 'Date *'), form_frame))
        self.checkup_date_edit = QDateEdit(form_frame)
        self.checkup_date_edit.setCalendarPopup(True)
        self.checkup_date_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.checkup_date_edit)

        form_layout.addWidget(QLabel(_t('checkup_form.chief_label', 'Chief Complaint *'), form_frame))
        self.checkup_chief_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.checkup_chief_edit)

        form_layout.addWidget(QLabel(_t('checkup_form.history_label', 'Medical History'), form_frame))
        self.checkup_history_edit = QTextEdit(form_frame)
        self.checkup_history_edit.setMaximumHeight(100)
        form_layout.addWidget(self.checkup_history_edit)

        form_layout.addWidget(QLabel(_t('checkup_form.exam_label', 'Examination'), form_frame))
        self.checkup_exam_edit = QTextEdit(form_frame)
        self.checkup_exam_edit.setMaximumHeight(100)
        form_layout.addWidget(self.checkup_exam_edit)

        form_layout.addWidget(QLabel(_t('checkup_form.diagnosis_label', 'Diagnosis *'), form_frame))
        self.checkup_diagnosis_edit = QTextEdit(form_frame)
        self.checkup_diagnosis_edit.setMaximumHeight(100)
        form_layout.addWidget(self.checkup_diagnosis_edit)

        form_layout.addWidget(QLabel(_t('checkup_form.plan_label', 'Treatment Plan'), form_frame))
        self.checkup_plan_edit = QTextEdit(form_frame)
        self.checkup_plan_edit.setMaximumHeight(100)
        form_layout.addWidget(self.checkup_plan_edit)

        form_layout.addWidget(QLabel(_t('checkup_form.notes_label', 'Notes'), form_frame))
        self.checkup_notes_edit = QTextEdit(form_frame)
        self.checkup_notes_edit.setMaximumHeight(100)
        form_layout.addWidget(self.checkup_notes_edit)

        # Buttons
        button_row = QHBoxLayout()
        clear_btn = QPushButton(_t('common.clear', 'Clear'), form_frame)
        clear_btn.clicked.connect(self.clear_checkup_form)
        self.checkup_save_btn = QPushButton(_t('checkup_form.add_button', 'Add Checkup'), form_frame)
        self.checkup_save_btn.clicked.connect(self.save_checkup)
        self.checkup_save_btn.setProperty("class", "primary")
        
        button_row.addWidget(clear_btn)
        button_row.addWidget(self.checkup_save_btn)
        button_row.addStretch(1)
        form_layout.addLayout(button_row)
        
        # Store frame reference for elevation effects
        self.checkup_form_frame = form_frame
        
        layout.addWidget(form_frame)
        layout.addStretch(1)

        self.checkup_edit_mode = False
        self.checkup_edit_id = None

        self.tabs.addTab(scroll, "🩺 " + _t('tabs.checkup', 'Checkup'))

    def _create_session_tab(self) -> None:
        """Create the add/edit session tab."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.session_title_label = QLabel(_t('session_form.title_add', 'Add New Session'), tab)
        self.session_title_label.setProperty("class", "h1")
        layout.addWidget(self.session_title_label)

        # Patient info display
        self.session_patient_label = QLabel(NO_PATIENT_SELECTED_TITLE, tab)
        self.session_patient_label.setWordWrap(True)
        layout.addWidget(self.session_patient_label)

        # Record selector (for edit mode)
        self.session_selector_frame = QFrame(tab)
        self.session_selector_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.session_selector_frame.setVisible(False)
        selector_layout = QVBoxLayout(self.session_selector_frame)
        selector_layout.addWidget(QLabel(_t('common.select_session_edit', 'Select Session to Edit'), self.session_selector_frame))
        self.session_selector_list = QListWidget(self.session_selector_frame)
        self.session_selector_list.itemClicked.connect(self.load_session_for_edit)
        selector_layout.addWidget(self.session_selector_list)
        layout.addWidget(self.session_selector_frame)

        # Form
        form_frame = QFrame(tab)
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(12)

        form_layout.addWidget(QLabel(_t('session_form.date_label', 'Date *'), form_frame))
        self.session_date_edit = QDateEdit(form_frame)
        self.session_date_edit.setCalendarPopup(True)
        self.session_date_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.session_date_edit)

        form_layout.addWidget(QLabel(_t('session_form.type_label', 'Type *'), form_frame))
        self.session_type_combo = QComboBox(form_frame)
        self.session_type_combo.addItems([
            _t('session_form.type_followup', 'Follow-up'),
            _t('session_form.type_initial', 'Initial'),
            _t('session_form.type_telemedicine', 'Telemedicine'),
            _t('session_form.type_emergency', 'Emergency'),
        ])
        form_layout.addWidget(self.session_type_combo)

        form_layout.addWidget(QLabel(_t('session_form.symptoms_label', 'Symptoms'), form_frame))
        self.session_symptoms_edit = QTextEdit(form_frame)
        self.session_symptoms_edit.setMaximumHeight(100)
        form_layout.addWidget(self.session_symptoms_edit)

        form_layout.addWidget(QLabel(_t('session_form.findings_label', 'Findings'), form_frame))
        self.session_findings_edit = QTextEdit(form_frame)
        self.session_findings_edit.setMaximumHeight(100)
        form_layout.addWidget(self.session_findings_edit)

        form_layout.addWidget(QLabel(_t('session_form.recommendations_label', 'Recommendations'), form_frame))
        self.session_reco_edit = QTextEdit(form_frame)
        self.session_reco_edit.setMaximumHeight(100)
        form_layout.addWidget(self.session_reco_edit)

        form_layout.addWidget(QLabel(_t('session_form.medications_label', 'Medications'), form_frame))
        self.session_meds_edit = QTextEdit(form_frame)
        self.session_meds_edit.setMaximumHeight(100)
        form_layout.addWidget(self.session_meds_edit)

        form_layout.addWidget(QLabel(_t('session_form.next_appointment_label', 'Next Appointment (optional)'), form_frame))
        self.session_next_date_edit = QDateEdit(form_frame)
        self.session_next_date_edit.setCalendarPopup(True)
        self.session_next_date_edit.setSpecialValueText("None")
        self.session_next_date_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.session_next_date_edit)

        form_layout.addWidget(QLabel(_t('session_form.notes_label', 'Notes'), form_frame))
        self.session_notes_edit = QTextEdit(form_frame)
        self.session_notes_edit.setMaximumHeight(100)
        form_layout.addWidget(self.session_notes_edit)

        # Buttons
        button_row = QHBoxLayout()
        clear_btn = QPushButton(_t('common.clear', 'Clear'), form_frame)
        clear_btn.clicked.connect(self.clear_session_form)
        self.session_save_btn = QPushButton(_t('session_form.add_button', 'Add Session'), form_frame)
        self.session_save_btn.clicked.connect(self.save_session)
        self.session_save_btn.setProperty("class", "primary")
        
        button_row.addWidget(clear_btn)
        button_row.addWidget(self.session_save_btn)
        button_row.addStretch(1)
        form_layout.addLayout(button_row)
        
        # Store frame reference for elevation effects
        self.session_form_frame = form_frame
        
        layout.addWidget(form_frame)
        layout.addStretch(1)

        self.session_edit_mode = False
        self.session_edit_id = None

        self.tabs.addTab(scroll, "💬 " + _t('tabs.session', 'Session'))

    def _create_medical_form_tab(self) -> None:
        """Create the adult medical consultation form tab."""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.medical_title_label = QLabel(_t('medical_form.title', 'Adult Medical Consultation Form'), tab)
        self.medical_title_label.setProperty("class", "h1")
        layout.addWidget(self.medical_title_label)

        # Patient info display
        self.medical_patient_label = QLabel(NO_PATIENT_SELECTED_TITLE, tab)
        self.medical_patient_label.setWordWrap(True)
        layout.addWidget(self.medical_patient_label)

        form_frame = QFrame(tab)
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(12)

        # Location / unit info
        form_layout.addWidget(QLabel(_t('medical_form.county_label', 'County (Județ)'), form_frame))
        self.medical_county_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_county_edit)

        form_layout.addWidget(QLabel(_t('medical_form.locality_label', 'Locality (Localitatea)'), form_frame))
        self.medical_locality_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_locality_edit)

        form_layout.addWidget(QLabel(_t('medical_form.health_unit_label', 'Health Unit (Unitatea sanitară)'), form_frame))
        self.medical_health_unit_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_health_unit_edit)

        # Registration / occupation
        form_layout.addWidget(QLabel(_t('medical_form.registration_date_label', 'Registration Date'), form_frame))
        self.medical_registration_date_edit = QDateEdit(form_frame)
        self.medical_registration_date_edit.setCalendarPopup(True)
        self.medical_registration_date_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.medical_registration_date_edit)

        form_layout.addWidget(QLabel(_t('medical_form.occupation_label', 'Occupation'), form_frame))
        self.medical_occupation_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_occupation_edit)

        form_layout.addWidget(QLabel(_t('medical_form.workplace_label', 'Workplace'), form_frame))
        self.medical_workplace_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_workplace_edit)

        form_layout.addWidget(QLabel(_t('medical_form.work_address_label', 'Workplace Address'), form_frame))
        self.medical_work_address_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_work_address_edit)

        form_layout.addWidget(QLabel(_t('medical_form.work_conditions_label', 'Working Conditions (Condiții de muncă)'), form_frame))
        self.medical_work_conditions_edit = QTextEdit(form_frame)
        self.medical_work_conditions_edit.setMaximumHeight(80)
        form_layout.addWidget(self.medical_work_conditions_edit)

        # Antecedents
        form_layout.addWidget(QLabel(_t('medical_form.hereditary_history_label', 'Hereditary History (Antecedente heredo-colaterale)'), form_frame))
        self.medical_hereditary_edit = QTextEdit(form_frame)
        self.medical_hereditary_edit.setMaximumHeight(80)
        form_layout.addWidget(self.medical_hereditary_edit)

        form_layout.addWidget(QLabel(_t('medical_form.personal_history_label', 'Personal History (Antecedente personale)'), form_frame))
        self.medical_personal_history_edit = QTextEdit(form_frame)
        self.medical_personal_history_edit.setMaximumHeight(80)
        form_layout.addWidget(self.medical_personal_history_edit)

        # Consultation details
        form_layout.addWidget(QLabel(_t('medical_form.consultation_date_label', 'Consultation Date *'), form_frame))
        self.medical_consultation_date_edit = QDateEdit(form_frame)
        self.medical_consultation_date_edit.setCalendarPopup(True)
        self.medical_consultation_date_edit.setDate(QDate.currentDate())
        form_layout.addWidget(self.medical_consultation_date_edit)

        form_layout.addWidget(QLabel(_t('medical_form.symptoms_label', 'Symptoms (Simptome)'), form_frame))
        self.medical_symptoms_edit = QTextEdit(form_frame)
        self.medical_symptoms_edit.setMaximumHeight(100)
        form_layout.addWidget(self.medical_symptoms_edit)

        form_layout.addWidget(QLabel(_t('medical_form.diagnosis_label', 'Diagnosis (Diagnostic)'), form_frame))
        self.medical_diagnosis_edit = QTextEdit(form_frame)
        self.medical_diagnosis_edit.setMaximumHeight(100)
        form_layout.addWidget(self.medical_diagnosis_edit)

        form_layout.addWidget(QLabel(_t('medical_form.icd_label', 'ICD Code (Cod)'), form_frame))
        self.medical_icd_code_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_icd_code_edit)

        form_layout.addWidget(QLabel(_t('medical_form.prescriptions_label', 'Prescriptions / Recommendations'), form_frame))
        self.medical_prescriptions_edit = QTextEdit(form_frame)
        self.medical_prescriptions_edit.setMaximumHeight(100)
        form_layout.addWidget(self.medical_prescriptions_edit)

        form_layout.addWidget(QLabel(_t('medical_form.sick_leave_days_label', 'Sick Leave Days (Zile concediu medical)'), form_frame))
        self.medical_sick_days_spin = QSpinBox(form_frame)
        self.medical_sick_days_spin.setRange(0, 365)
        form_layout.addWidget(self.medical_sick_days_spin)

        form_layout.addWidget(QLabel(_t('medical_form.certificate_label', 'Certificate Number (Nr. certificat)'), form_frame))
        self.medical_certificate_edit = QLineEdit(form_frame)
        form_layout.addWidget(self.medical_certificate_edit)

        form_layout.addWidget(QLabel(_t('medical_form.notes_label', 'Notes'), form_frame))
        self.medical_notes_edit = QTextEdit(form_frame)
        self.medical_notes_edit.setMaximumHeight(80)
        form_layout.addWidget(self.medical_notes_edit)

        # Buttons
        button_row = QHBoxLayout()
        clear_btn = QPushButton(_t('common.clear', 'Clear'), form_frame)
        clear_btn.clicked.connect(self.clear_medical_form)
        save_btn = QPushButton(_t('medical_form.save_export_button', 'Save & Export PDF'), form_frame)
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self.save_medical_form)

        button_row.addWidget(clear_btn)
        button_row.addWidget(save_btn)
        button_row.addStretch(1)
        form_layout.addLayout(button_row)

        self.medical_form_frame = form_frame

        layout.addWidget(form_frame)
        layout.addStretch(1)

        self.tabs.addTab(scroll, "📝 " + _t('tabs.medical_form', 'Medical Form'))

    def _setup_shortcuts(self) -> None:
        """Set up keyboard shortcuts for quick navigation."""
        # Tab navigation shortcuts
        QShortcut(QKeySequence("Ctrl+1"), self, lambda: self.tabs.setCurrentIndex(0))
        QShortcut(QKeySequence("Ctrl+2"), self, lambda: self.tabs.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+3"), self, lambda: self.tabs.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+4"), self, lambda: self.tabs.setCurrentIndex(3))
        QShortcut(QKeySequence("Ctrl+5"), self, lambda: self.tabs.setCurrentIndex(4))
        
        # Quick actions
        QShortcut(QKeySequence("Ctrl+N"), self, lambda: self.tabs.setCurrentIndex(1))  # New patient
        QShortcut(QKeySequence("Ctrl+R"), self, self.refresh_patients)  # Refresh
        QShortcut(QKeySequence("Ctrl+E"), self, self.export_pdf)  # Export PDF
        QShortcut(QKeySequence("F5"), self, self.refresh_patients)  # Refresh (alternative)
        QShortcut(QKeySequence("Ctrl+T"), self, self.toggle_theme)  # Toggle theme

    def apply_theme(self, theme: Literal["light", "dark"]) -> None:
        """Apply Material Design theme to the window."""
        self.current_theme = theme
        dark_mode = (theme == "dark")
        
        # Apply main stylesheet
        stylesheet = get_material_stylesheet(theme)
        self.setStyleSheet(stylesheet)
        
        # Apply theme toggle button style separately
        toggle_style = get_theme_toggle_button_style(theme)
        self.theme_toggle_btn.setStyleSheet(toggle_style)
        
        # Apply elevation effects to form frames if they exist
        if hasattr(self, 'patient_form_frame'):
            apply_card_elevation(self.patient_form_frame, dark_mode)
        if hasattr(self, 'checkup_form_frame'):
            apply_card_elevation(self.checkup_form_frame, dark_mode)
        if hasattr(self, 'session_form_frame'):
            apply_card_elevation(self.session_form_frame, dark_mode)
        if hasattr(self, 'patient_info_frame'):
            apply_card_elevation(self.patient_info_frame, dark_mode)
        if hasattr(self, 'medical_form_frame'):
            apply_card_elevation(self.medical_form_frame, dark_mode)
        
        # Update button text
        self._update_theme_button_text()
        
        # Save preference
        self.settings.setValue('theme', theme)
        
        # Show status message
        theme_name = _t('common.dark_mode', 'Dark') if theme == 'dark' else _t('common.light_mode', 'Light')
        self.statusBar().showMessage(_t('common.theme_activated', '{theme} mode activated').format(theme=theme_name), 2000)
    
    def _update_theme_button_text(self) -> None:
        """Update theme toggle button text based on current theme."""
        if self.current_theme == "light":
            self.theme_toggle_btn.setText("🌙 " + _t('common.dark_mode', 'Dark Mode'))
            self.theme_toggle_btn.setToolTip(_t('common.dark_mode_tooltip', 'Switch to dark mode (Ctrl+T)'))
        else:
            self.theme_toggle_btn.setText("☀️ " + _t('common.light_mode', 'Light Mode'))
            self.theme_toggle_btn.setToolTip(_t('common.light_mode_tooltip', 'Switch to light mode (Ctrl+T)'))
    
    def toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
    
    def change_language(self) -> None:
        """Show language selection dialog."""
        current_lang = self.language_manager.get_current_language()
        dialog = LanguageSelectorDialog(current_lang, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_lang = dialog.get_selected_language()
            if new_lang != current_lang:
                self.language_manager.change_language(new_lang)
                self._reload_ui_text()
                QMessageBox.information(
                    self,
                    _t('language.select_language', 'Select Language'),
                    _t('language.language_changed', 'Language changed successfully!')
                )
    
    def _reload_ui_text(self) -> None:
        """Reload all UI text after language change."""
        # Update window title
        self.setWindowTitle(_t('app.title', 'Psychological Records'))
        
        # Update tab titles
        self.tabs.setTabText(0, "📋 " + _t('tabs.patients', 'Patients'))
        self.tabs.setTabText(1, "➕ " + _t('tabs.add_patient', 'Add Patient'))
        self.tabs.setTabText(2, "🩺 " + _t('tabs.checkup', 'Checkup'))
        self.tabs.setTabText(3, "💬 " + _t('tabs.session', 'Session'))
        self.tabs.setTabText(4, "📝 " + _t('tabs.medical_form', 'Medical Form'))
        
        # Update buttons and labels
        self.language_btn.setText(f"🌍 {self.language_manager.get_language_display_name(self.language_manager.get_current_language())}")
        self.language_btn.setToolTip(_t('menu.change_language', 'Change Language'))
        self._update_theme_button_text()
        
        # Update tab accessibility
        self._update_tab_accessibility()
        
        # Refresh current view if patient is selected
        if self.current_patient_id:
            self.load_records_for_selected()

    def _update_tab_accessibility(self) -> None:
        """Enable or disable tabs based on whether a patient is selected."""
        has_patient = self.current_patient_id is not None
        
        # Tabs that require a patient selection: Checkup (index 2), Session (index 3), Medical Form (index 4)
        self.tabs.setTabEnabled(2, has_patient)  # Checkup tab
        self.tabs.setTabEnabled(3, has_patient)  # Session tab
        self.tabs.setTabEnabled(4, has_patient)  # Medical form tab
        
        # Update tab tooltips
        if not has_patient:
            self.tabs.setTabToolTip(2, _t('tabs.checkup_disabled', 'Select a patient first to add/edit checkups'))
            self.tabs.setTabToolTip(3, _t('tabs.session_disabled', 'Select a patient first to add/edit sessions'))
            self.tabs.setTabToolTip(4, _t('tabs.medical_form_disabled', 'Select a patient first to complete medical consultation forms'))
        else:
            self.tabs.setTabToolTip(2, _t('tabs.checkup_tooltip', 'Add or edit medical checkups for the selected patient'))
            self.tabs.setTabToolTip(3, _t('tabs.session_tooltip', 'Add or edit therapy sessions for the selected patient'))
            self.tabs.setTabToolTip(4, _t('tabs.medical_form_tooltip', 'Record and export adult medical consultation forms for the selected patient'))
    
    def _on_tab_changed(self, index: int) -> None:
        """Handle tab changes."""
        # If user tries to access a patient-dependent tab without selecting a patient,
        # show a message and switch back to patients tab
        if index in (2, 3, 4) and self.current_patient_id is None:
            QMessageBox.information(
                self,
                _t('common.select_patient_first', 'No Patient Selected'),
                _t('common.select_tab_info', 'Please select a patient from the Patients tab before adding or editing records.')
            )
            self.tabs.setCurrentIndex(0)  # Go back to Patients tab
            return
        # Combine medical record into Checkup/Session tabs: show existing records when switching
        if index == 2 and self.current_patient_id is not None:
            self._populate_checkup_list_for_tab()
        elif index == 3 and self.current_patient_id is not None:
            self._populate_session_list_for_tab()

    def _populate_checkup_list_for_tab(self) -> None:
        """Populate checkup selector with patient's checkups so record data appears in Checkup tab."""
        if getattr(self, "db", None) is None or self.current_patient_id is None:
            return
        assessments = self.db.get_assessments_for_person(self.current_patient_id)
        self.checkup_selector_list.clear()
        for a in assessments:
            label = f"{a[1]} - {a[5] or 'No diagnosis'}"
            self.checkup_selector_list.addItem(label)
            self.checkup_selector_list.item(self.checkup_selector_list.count() - 1).setData(Qt.ItemDataRole.UserRole, a[0])
        self.checkup_selector_frame.setVisible(len(assessments) > 0)
        self._update_checkup_patient_label()

    def _populate_session_list_for_tab(self) -> None:
        """Populate session selector with patient's sessions so record data appears in Session tab."""
        if getattr(self, "db", None) is None or self.current_patient_id is None:
            return
        consultations = self.db.get_consultations_for_person(self.current_patient_id)
        self.session_selector_list.clear()
        for c in consultations:
            label = f"{c[1]} - {c[2]}"
            self.session_selector_list.addItem(label)
            self.session_selector_list.item(self.session_selector_list.count() - 1).setData(Qt.ItemDataRole.UserRole, c[0])
        self.session_selector_frame.setVisible(len(consultations) > 0)
        self._update_session_patient_label()

    # ===== Database Integration =====

    def attach_db_and_load(self) -> None:
        """Attach database and load initial data."""
        if getattr(self, "db", None) is None:
            return
        self._initialized = True
        self.refresh_patients()

    def refresh_patients(self) -> None:
        """Reload patient list from database."""
        if getattr(self, "db", None) is None:
            return
        persons = self.db.get_all_persons()
        self.table.setRowCount(len(persons))
        
        for row_index, (pid, name, cnp, created_at) in enumerate(persons):
            # ID
            id_item = QTableWidgetItem(str(pid))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_index, 0, id_item)
            
            # Name
            self.table.setItem(row_index, 1, QTableWidgetItem(name))
            
            # CNP
            cnp_item = QTableWidgetItem(cnp)
            cnp_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_index, 2, cnp_item)
            
            # Registered date
            date_item = QTableWidgetItem(created_at[:10] if created_at else "")
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_index, 3, date_item)
            
            # Records count
            record = self.db.get_person_complete_record(pid)
            checkup_count = len(record.get("assessments", [])) if record else 0
            session_count = len(record.get("consultations", [])) if record else 0
            form_count = len(record.get("medical_forms", [])) if record else 0
            total_records = checkup_count + session_count + form_count
            
            records_item = QTableWidgetItem(f"{total_records}")
            records_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_index, 4, records_item)

        self.statusBar().showMessage(f"Loaded {len(persons)} patients", 1500)
        self.load_records_for_selected()

    def _get_selected_person_id(self) -> int | None:
        """Get the currently selected patient ID."""
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            return None
        row = selection[0].row()
        item = self.table.item(row, 0)
        try:
            return int(item.text()) if item else None
        except Exception:
            return None

    def load_records_for_selected(self) -> None:
        """Load and display records for the selected patient."""
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        self.current_patient_id = person_id
        
        # Update tab accessibility based on patient selection
        self._update_tab_accessibility()
        
        if person_id is None:
            self.patient_name_label.setText(NO_PATIENT_SELECTED_TITLE)
            self.patient_details_label.setText("Select a patient from the table to view their records")
            self.records_view.setPlainText(_t('main_window.select_person_records', 'Select a patient to view records.'))
            return
            
        record = self.db.get_person_complete_record(person_id)
        if not record:
            self.records_view.setPlainText(_t('psychological_records.no_data_found', 'No records found.'))
            return
            
        person = record.get("person")
        assessments = record.get("assessments", [])
        consultations = record.get("consultations", [])
        medical_forms = record.get("medical_forms", [])

        # Update patient info card
        self.patient_name_label.setText(person[1])
        self.patient_details_label.setText(
            f"CNP: {person[2]} | Registered: {person[3][:10] if person[3] else 'Unknown'} | "
            f"Records: {len(assessments) + len(consultations) + len(medical_forms)} total"
        )

        # Build combined record view: Patient, Checkups, Sessions, Medical Forms
        html_lines = []
        html_lines.append("<html><body style='font-family: sans-serif;'>")

        # Patient section (combine medical record into patient section)
        section_patient = _t('main_window.section_patient', 'Patient')
        html_lines.append(f"<h3 style='color: #607D8B; margin-top: 0;'>👤 {section_patient}</h3>")
        html_lines.append("<div style='margin: 10px 0; padding: 10px; background: rgba(96, 125, 139, 0.08); border-left: 3px solid #607D8B;'>")
        html_lines.append(f"<strong>{_t('main_window.name', 'Name')}:</strong> {person[1]}<br>")
        html_lines.append(f"<strong>{_t('main_window.cnp', 'CNP')}:</strong> {person[2]}<br>")
        reg = person[3][:10] if person[3] else '—'
        html_lines.append(f"<strong>{_t('main_window.registered', 'Registered')}:</strong> {reg}</div>")

        # Checkups section
        section_checkups = _t('main_window.section_checkups', 'Checkups')
        html_lines.append(f"<h3 style='color: #2196F3; margin-top: 20px;'>🩺 {section_checkups} ({len(assessments)})</h3>")
        if assessments:
            for a in assessments:
                html_lines.append("<div style='margin: 10px 0; padding: 10px; background: rgba(33, 150, 243, 0.05); border-left: 3px solid #2196F3;'>")
                html_lines.append(f"<strong>Date:</strong> {a[1]}<br>")
                html_lines.append(f"<strong>Chief Complaint:</strong> {a[2] or 'N/A'}<br>")
                html_lines.append(f"<strong>Diagnosis:</strong> {a[5] or 'N/A'}<br>")
                html_lines.append(f"<strong>Plan:</strong> {a[6] or 'N/A'}<br>")
                if len(a) > 8 and a[8]:
                    html_lines.append(f"<strong>Notes:</strong> {a[8]}")
                html_lines.append("</div>")
        else:
            html_lines.append(f"<p><em>{_t('main_window.no_checkups_recorded', 'No checkups recorded')}</em></p>")

        # Sessions section (aligned with Session tab)
        section_sessions = _t('main_window.section_sessions', 'Sessions')
        html_lines.append(f"<h3 style='color: #4CAF50; margin-top: 20px;'>💬 {section_sessions} ({len(consultations)})</h3>")
        if consultations:
            for c in consultations:
                html_lines.append("<div style='margin: 10px 0; padding: 10px; background: rgba(76, 175, 80, 0.05); border-left: 3px solid #4CAF50;'>")
                html_lines.append(f"<strong>Date:</strong> {c[1]} <span style='background: #4CAF50; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;'>{c[2]}</span><br>")
                html_lines.append(f"<strong>Symptoms:</strong> {c[3] or 'N/A'}<br>")
                html_lines.append(f"<strong>Findings:</strong> {c[4] or 'N/A'}<br>")
                html_lines.append(f"<strong>Recommendations:</strong> {c[6] or 'N/A'}<br>")
                if c[7]:
                    html_lines.append(f"<strong>Next Appointment:</strong> {c[7]}<br>")
                if len(c) > 9 and c[9]:
                    html_lines.append(f"<strong>Notes:</strong> {c[9]}")
                html_lines.append("</div>")
        else:
            html_lines.append(f"<p><em>{_t('main_window.no_sessions_recorded', 'No sessions recorded')}</em></p>")

        # Medical Forms section
        section_forms = _t('main_window.section_medical_forms', 'Medical Forms')
        html_lines.append(f"<h3 style='color: #9C27B0; margin-top: 20px;'>📝 {section_forms} ({len(medical_forms)})</h3>")
        if medical_forms:
            for f_rec in medical_forms:
                (
                    form_id,
                    _person_id,
                    county,
                    locality,
                    health_unit,
                    registration_date,
                    occupation,
                    workplace,
                    work_address,
                    work_conditions,
                    hereditary_history,
                    personal_history,
                    consultation_date,
                    symptoms,
                    diagnosis,
                    icd_code,
                    prescriptions,
                    recommendations,
                    sick_leave_days,
                    certificate_number,
                    notes,
                    created_at,
                    updated_at,
                ) = f_rec
                html_lines.append("<div style='margin: 10px 0; padding: 10px; background: rgba(156, 39, 176, 0.05); border-left: 3px solid #9C27B0;'>")
                html_lines.append(f"<strong>Date consultație:</strong> {consultation_date or 'N/A'}<br>")
                html_lines.append(f"<strong>Unitate sanitară:</strong> {health_unit or 'N/A'}<br>")
                html_lines.append(f"<strong>Simptome:</strong> {symptoms or 'N/A'}<br>")
                html_lines.append(f"<strong>Diagnostic:</strong> {diagnosis or 'N/A'} (cod: {icd_code or '-'})<br>")
                html_lines.append(f"<strong>Prescrieri / Recomandări:</strong> {prescriptions or recommendations or 'N/A'}<br>")
                if sick_leave_days is not None:
                    html_lines.append(f"<strong>Zile concediu medical:</strong> {sick_leave_days}<br>")
                if certificate_number:
                    html_lines.append(f"<strong>Nr. certificat:</strong> {certificate_number}<br>")
                if notes:
                    html_lines.append(f"<strong>Note:</strong> {notes}")
                html_lines.append("</div>")
        else:
            html_lines.append(f"<p><em>{_t('main_window.no_medical_forms_recorded', 'No medical forms recorded')}</em></p>")

        html_lines.append("</body></html>")
        self.records_view.setHtml("\n".join(html_lines))

    # ===== Patient Management =====

    def clear_patient_form(self) -> None:
        """Clear the patient form."""
        self.patient_name_edit.clear()
        self.patient_cnp_edit.clear()

    def save_patient(self) -> None:
        """Save a new patient."""
        if getattr(self, "db", None) is None:
            return
            
        name = self.patient_name_edit.text().strip()
        cnp = self.patient_cnp_edit.text().strip()
        
        if not name or not cnp:
            QMessageBox.warning(self, "Required Fields", "Name and CNP are required.")
            return
            
        if not self.db.add_person(name, cnp):
            QMessageBox.critical(self, "Error", "Failed to add patient (duplicate CNP?)")
            return
            
        self.clear_patient_form()
        self.refresh_patients()
        self.statusBar().showMessage("Patient added successfully", 2000)
        self.tabs.setCurrentIndex(0)  # Go back to patients tab

    # ===== Checkup Management =====

    def start_add_checkup(self) -> None:
        """Start adding a new checkup."""
        if self.current_patient_id is None:
            QMessageBox.warning(self, NO_PATIENT_TITLE, SELECT_PATIENT_MSG)
            return
            
        self.checkup_edit_mode = False
        self.checkup_edit_id = None
        self.checkup_title_label.setText("Add New Checkup")
        self.checkup_save_btn.setText("Add Checkup")
        self.checkup_selector_frame.setVisible(False)
        self.clear_checkup_form()
        self._update_checkup_patient_label()
        self.tabs.setCurrentIndex(2)  # Switch to checkup tab

    def start_edit_checkup(self) -> None:
        """Start editing an existing checkup."""
        if self.current_patient_id is None:
            QMessageBox.warning(self, NO_PATIENT_TITLE, SELECT_PATIENT_MSG)
            return
            
        assessments = self.db.get_assessments_for_person(self.current_patient_id)
        if not assessments:
            QMessageBox.information(self, "No Checkups", "This patient has no checkups to edit.")
            return
            
        self.checkup_edit_mode = True
        self.checkup_title_label.setText("Edit Checkup")
        self.checkup_save_btn.setText("Update Checkup")
        self.checkup_selector_frame.setVisible(True)
        self._update_checkup_patient_label()
        
        # Populate selector
        self.checkup_selector_list.clear()
        for a in assessments:
            label = f"{a[1]} - {a[5] or 'No diagnosis'}"
            self.checkup_selector_list.addItem(label)
            # Store the assessment ID in the item
            self.checkup_selector_list.item(self.checkup_selector_list.count() - 1).setData(Qt.ItemDataRole.UserRole, a[0])
        
        self.tabs.setCurrentIndex(2)  # Switch to checkup tab

    def load_checkup_for_edit(self, item) -> None:
        """Load checkup data into form for editing."""
        checkup_id = item.data(Qt.ItemDataRole.UserRole)
        self.checkup_edit_id = checkup_id
        
        assessments = self.db.get_assessments_for_person(self.current_patient_id)
        current = next((a for a in assessments if a[0] == checkup_id), None)
        if not current:
            return
            
        # Load data into form: (id, date, chief, history, exam, diagnosis, plan, person_id, notes)
        self.checkup_date_edit.setDate(QDate.fromString(current[1], "yyyy-MM-dd"))
        self.checkup_chief_edit.setText(current[2] or "")
        self.checkup_history_edit.setPlainText(current[3] or "")
        self.checkup_exam_edit.setPlainText(current[4] or "")
        self.checkup_diagnosis_edit.setPlainText(current[5] or "")
        self.checkup_plan_edit.setPlainText(current[6] or "")
        self.checkup_notes_edit.setPlainText(current[8] if len(current) > 8 else "")

    def clear_checkup_form(self) -> None:
        """Clear the checkup form."""
        self.checkup_date_edit.setDate(QDate.currentDate())
        self.checkup_chief_edit.clear()
        self.checkup_history_edit.clear()
        self.checkup_exam_edit.clear()
        self.checkup_diagnosis_edit.clear()
        self.checkup_plan_edit.clear()
        self.checkup_notes_edit.clear()

    def _update_checkup_patient_label(self) -> None:
        """Update the patient info label in checkup tab."""
        if self.current_patient_id and hasattr(self, 'db'):
            record = self.db.get_person_complete_record(self.current_patient_id)
            if record:
                person = record.get("person")
                self.checkup_patient_label.setText(f"Patient: {person[1]} (CNP: {person[2]})")
                return
        self.checkup_patient_label.setText(NO_PATIENT_SELECTED_TITLE)

    def save_checkup(self) -> None:
        """Save or update a checkup."""
        if getattr(self, "db", None) is None or self.current_patient_id is None:
            return
            
        date = self.checkup_date_edit.date().toString("yyyy-MM-dd")
        chief = self.checkup_chief_edit.text().strip()
        history = self.checkup_history_edit.toPlainText().strip()
        exam = self.checkup_exam_edit.toPlainText().strip()
        diagnosis = self.checkup_diagnosis_edit.toPlainText().strip()
        plan = self.checkup_plan_edit.toPlainText().strip()
        notes = self.checkup_notes_edit.toPlainText().strip()
        
        if not chief or not diagnosis:
            QMessageBox.warning(self, "Required Fields", "Chief complaint and diagnosis are required.")
            return
            
        if self.checkup_edit_mode and self.checkup_edit_id:
            # Update existing
            self.db.update_assessment(
                self.checkup_edit_id,
                date,
                chief,
                history,
                exam,
                diagnosis,
                plan,
                notes,
            )
            self.statusBar().showMessage("Checkup updated successfully", 2000)
        else:
            # Add new
            if not self.db.add_assessment(
                self.current_patient_id,
                date,
                chief,
                history,
                exam,
                diagnosis,
                plan,
                notes,
            ):
                QMessageBox.critical(self, "Error", "Failed to add checkup")
                return
            self.statusBar().showMessage("Checkup added successfully", 2000)
            
        self.clear_checkup_form()
        self.load_records_for_selected()
        self.tabs.setCurrentIndex(0)  # Go back to patients tab

    # ===== Session Management =====

    def start_add_session(self) -> None:
        """Start adding a new session."""
        if self.current_patient_id is None:
            QMessageBox.warning(self, NO_PATIENT_TITLE, SELECT_PATIENT_MSG)
            return
            
        self.session_edit_mode = False
        self.session_edit_id = None
        self.session_title_label.setText("Add New Session")
        self.session_save_btn.setText("Add Session")
        self.session_selector_frame.setVisible(False)
        self.clear_session_form()
        self._update_session_patient_label()
        self.tabs.setCurrentIndex(3)  # Switch to session tab

    def start_edit_session(self) -> None:
        """Start editing an existing session."""
        if self.current_patient_id is None:
            QMessageBox.warning(self, NO_PATIENT_TITLE, SELECT_PATIENT_MSG)
            return
            
        consultations = self.db.get_consultations_for_person(self.current_patient_id)
        if not consultations:
            QMessageBox.information(self, "No Sessions", "This patient has no sessions to edit.")
            return
            
        self.session_edit_mode = True
        self.session_title_label.setText("Edit Session")
        self.session_save_btn.setText("Update Session")
        self.session_selector_frame.setVisible(True)
        self._update_session_patient_label()
        
        # Populate selector
        self.session_selector_list.clear()
        for c in consultations:
            label = f"{c[1]} - {c[2]}"
            self.session_selector_list.addItem(label)
            # Store the consultation ID in the item
            self.session_selector_list.item(self.session_selector_list.count() - 1).setData(Qt.ItemDataRole.UserRole, c[0])
        
        self.tabs.setCurrentIndex(3)  # Switch to session tab

    def load_session_for_edit(self, item) -> None:
        """Load session data into form for editing."""
        session_id = item.data(Qt.ItemDataRole.UserRole)
        self.session_edit_id = session_id
        
        consultations = self.db.get_consultations_for_person(self.current_patient_id)
        current = next((c for c in consultations if c[0] == session_id), None)
        if not current:
            return
            
        # Load data into form: (id, date, type, symptoms, findings, medications, reco, next_appt, person_id, notes)
        self.session_date_edit.setDate(QDate.fromString(current[1], "yyyy-MM-dd"))
        self.session_type_combo.setCurrentText(current[2] or "Follow-up")
        self.session_symptoms_edit.setPlainText(current[3] or "")
        self.session_findings_edit.setPlainText(current[4] or "")
        self.session_meds_edit.setPlainText(current[5] or "")
        self.session_reco_edit.setPlainText(current[6] or "")
        if current[7]:
            self.session_next_date_edit.setDate(QDate.fromString(current[7], "yyyy-MM-dd"))
        self.session_notes_edit.setPlainText(current[9] if len(current) > 9 else "")

    def clear_session_form(self) -> None:
        """Clear the session form."""
        self.session_date_edit.setDate(QDate.currentDate())
        self.session_type_combo.setCurrentIndex(0)
        self.session_symptoms_edit.clear()
        self.session_findings_edit.clear()
        self.session_reco_edit.clear()
        self.session_meds_edit.clear()
        self.session_next_date_edit.setDate(QDate.currentDate())
        self.session_notes_edit.clear()

    def _update_session_patient_label(self) -> None:
        """Update the patient info label in session tab."""
        if self.current_patient_id and hasattr(self, 'db'):
            record = self.db.get_person_complete_record(self.current_patient_id)
            if record:
                person = record.get("person")
                self.session_patient_label.setText(f"Patient: {person[1]} (CNP: {person[2]})")
                return
        self.session_patient_label.setText(NO_PATIENT_SELECTED_TITLE)

    def save_session(self) -> None:
        """Save or update a session."""
        if getattr(self, "db", None) is None or self.current_patient_id is None:
            return
            
        date = self.session_date_edit.date().toString("yyyy-MM-dd")
        session_type = self.session_type_combo.currentText()
        symptoms = self.session_symptoms_edit.toPlainText().strip()
        findings = self.session_findings_edit.toPlainText().strip()
        reco = self.session_reco_edit.toPlainText().strip()
        meds = self.session_meds_edit.toPlainText().strip()
        next_appt = self.session_next_date_edit.date().toString("yyyy-MM-dd")
        notes = self.session_notes_edit.toPlainText().strip()
        
        if self.session_edit_mode and self.session_edit_id:
            # Update existing
            self.db.update_consultation(
                self.session_edit_id,
                date,
                session_type,
                symptoms,
                findings,
                reco,
                meds,
                next_appt,
                notes,
            )
            self.statusBar().showMessage("Session updated successfully", 2000)
        else:
            # Add new
            if not self.db.add_consultation(
                self.current_patient_id,
                date,
                session_type,
                symptoms,
                findings,
                reco,
                meds,
                next_appt,
                notes,
            ):
                QMessageBox.critical(self, "Error", "Failed to add session")
                return
            self.statusBar().showMessage("Session added successfully", 2000)
            
        self.clear_session_form()
        self.load_records_for_selected()
        self.tabs.setCurrentIndex(0)  # Go back to patients tab

    # ===== Adult Medical Consultation Form Management =====

    def start_medical_form(self) -> None:
        """Start filling a new adult medical consultation form."""
        if self.current_patient_id is None:
            QMessageBox.warning(self, NO_PATIENT_TITLE, SELECT_PATIENT_MSG)
            return
        self._update_medical_patient_label()
        self._load_latest_medical_form()
        self.tabs.setCurrentIndex(4)  # Medical form tab

    def _load_latest_medical_form(self) -> None:
        """Load the most recent adult medical consultation into the form if it exists."""
        if self.current_patient_id is None or not hasattr(self, "db"):
            self.clear_medical_form()
            return
        records = self.db.get_adult_medical_consultations_for_person(self.current_patient_id)
        if not records:
            self.clear_medical_form()
            return
        latest = records[0]
        (
            _form_id,
            _person_id,
            county,
            locality,
            health_unit,
            registration_date,
            occupation,
            workplace,
            work_address,
            work_conditions,
            hereditary_history,
            personal_history,
            consultation_date,
            symptoms,
            diagnosis,
            icd_code,
            prescriptions,
            _recommendations,
            sick_leave_days,
            certificate_number,
            notes,
            _created_at,
            _updated_at,
        ) = latest

        self.medical_county_edit.setText(county or "")
        self.medical_locality_edit.setText(locality or "")
        self.medical_health_unit_edit.setText(health_unit or "")
        if registration_date:
            self.medical_registration_date_edit.setDate(QDate.fromString(registration_date, "yyyy-MM-dd"))
        else:
            self.medical_registration_date_edit.setDate(QDate.currentDate())
        self.medical_occupation_edit.setText(occupation or "")
        self.medical_workplace_edit.setText(workplace or "")
        self.medical_work_address_edit.setText(work_address or "")
        self.medical_work_conditions_edit.setPlainText(work_conditions or "")
        self.medical_hereditary_edit.setPlainText(hereditary_history or "")
        self.medical_personal_history_edit.setPlainText(personal_history or "")
        if consultation_date:
            self.medical_consultation_date_edit.setDate(QDate.fromString(consultation_date, "yyyy-MM-dd"))
        else:
            self.medical_consultation_date_edit.setDate(QDate.currentDate())
        self.medical_symptoms_edit.setPlainText(symptoms or "")
        self.medical_diagnosis_edit.setPlainText(diagnosis or "")
        self.medical_icd_code_edit.setText(icd_code or "")
        self.medical_prescriptions_edit.setPlainText(prescriptions or "")
        self.medical_sick_days_spin.setValue(sick_leave_days or 0)
        self.medical_certificate_edit.setText(certificate_number or "")
        self.medical_notes_edit.setPlainText(notes or "")

    def _update_medical_patient_label(self) -> None:
        """Update the patient info label in the medical form tab."""
        if self.current_patient_id and hasattr(self, "db"):
            record = self.db.get_person_complete_record(self.current_patient_id)
            if record:
                person = record.get("person")
                self.medical_patient_label.setText(f"Patient: {person[1]} (CNP: {person[2]})")
                return
        self.medical_patient_label.setText(NO_PATIENT_SELECTED_TITLE)

    def clear_medical_form(self) -> None:
        """Clear the adult medical consultation form."""
        self.medical_county_edit.clear()
        self.medical_locality_edit.clear()
        self.medical_health_unit_edit.clear()
        self.medical_registration_date_edit.setDate(QDate.currentDate())
        self.medical_occupation_edit.clear()
        self.medical_workplace_edit.clear()
        self.medical_work_address_edit.clear()
        self.medical_work_conditions_edit.clear()
        self.medical_hereditary_edit.clear()
        self.medical_personal_history_edit.clear()
        self.medical_consultation_date_edit.setDate(QDate.currentDate())
        self.medical_symptoms_edit.clear()
        self.medical_diagnosis_edit.clear()
        self.medical_icd_code_edit.clear()
        self.medical_prescriptions_edit.clear()
        self.medical_sick_days_spin.setValue(0)
        self.medical_certificate_edit.clear()
        self.medical_notes_edit.clear()

    def save_medical_form(self) -> None:
        """Save the medical form to the database and export a PDF."""
        if getattr(self, "db", None) is None or self.current_patient_id is None:
            return

        consultation_date = self.medical_consultation_date_edit.date().toString("yyyy-MM-dd")
        if not consultation_date:
            QMessageBox.warning(self, _t('common.required_fields', 'Required Fields'), _t('medical_form.required_date_message', 'Consultation date is required.'))
            return

        county = self.medical_county_edit.text().strip()
        locality = self.medical_locality_edit.text().strip()
        health_unit = self.medical_health_unit_edit.text().strip()
        registration_date = self.medical_registration_date_edit.date().toString("yyyy-MM-dd")
        occupation = self.medical_occupation_edit.text().strip()
        workplace = self.medical_workplace_edit.text().strip()
        work_address = self.medical_work_address_edit.text().strip()
        work_conditions = self.medical_work_conditions_edit.toPlainText().strip()
        hereditary_history = self.medical_hereditary_edit.toPlainText().strip()
        personal_history = self.medical_personal_history_edit.toPlainText().strip()
        symptoms = self.medical_symptoms_edit.toPlainText().strip()
        diagnosis = self.medical_diagnosis_edit.toPlainText().strip()
        icd_code = self.medical_icd_code_edit.text().strip()
        prescriptions = self.medical_prescriptions_edit.toPlainText().strip()
        sick_leave_days = self.medical_sick_days_spin.value()
        certificate_number = self.medical_certificate_edit.text().strip()
        notes = self.medical_notes_edit.toPlainText().strip()

        sick_leave_days_value = sick_leave_days if sick_leave_days > 0 else None

        if not self.db.add_adult_medical_consultation(
            self.current_patient_id,
            consultation_date,
            county=county,
            locality=locality,
            health_unit=health_unit,
            registration_date=registration_date,
            occupation=occupation,
            workplace=workplace,
            work_address=work_address,
            work_conditions=work_conditions,
            hereditary_history=hereditary_history,
            personal_history=personal_history,
            symptoms=symptoms,
            diagnosis=diagnosis,
            icd_code=icd_code,
            prescriptions=prescriptions,
            recommendations="",
            sick_leave_days=sick_leave_days_value,
            certificate_number=certificate_number,
            notes=notes,
        ):
            QMessageBox.critical(self, "Error", "Failed to save medical consultation form.")
            return

        # Generate PDF based on current data
        record = self.db.get_person_complete_record(self.current_patient_id)
        person = record.get("person") if record else None
        if not person:
            QMessageBox.critical(self, "Error", "Failed to load patient details for PDF.")
            return

        form_data = {
            "county": county,
            "locality": locality,
            "health_unit": health_unit,
            "registration_date": registration_date,
            "occupation": occupation,
            "workplace": workplace,
            "work_address": work_address,
            "work_conditions": work_conditions,
            "hereditary_history": hereditary_history,
            "personal_history": personal_history,
            "consultation_date": consultation_date,
            "symptoms": symptoms,
            "diagnosis": diagnosis,
            "icd_code": icd_code,
            "prescriptions": prescriptions,
            "recommendations": "",
            "sick_leave_days": sick_leave_days_value,
            "certificate_number": certificate_number,
            "notes": notes,
        }

        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        safe_name = (person[1] or "patient").replace(" ", "_")
        pdf_path = os.path.join(out_dir, f"MedicalForm_{safe_name}_{consultation_date}.pdf")

        try:
            generate_medical_consultation_form(person, form_data, pdf_path)
            self.statusBar().showMessage(f"Medical consultation form saved and exported → {pdf_path}", 3000)
        except Exception:
            self.statusBar().showMessage("Failed to export medical consultation PDF", 3000)

        self.clear_medical_form()
        self.load_records_for_selected()
        self.tabs.setCurrentIndex(0)

    # ===== PDF Export =====

    def export_pdf(self) -> None:
        """Export PDF report for selected patient."""
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage("Select a patient first", 2000)
            return
        record = self.db.get_person_complete_record(person_id)
        if not record:
            self.statusBar().showMessage(_t('psychological_records.no_data_found', 'No data to export'), 2000)
            return
        person = record.get("person")
        assessments = record.get("assessments", [])
        consultations = record.get("consultations", [])
        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        safe_name = (person[1] or "patient").replace(" ", "_")
        path = os.path.join(out_dir, f"Report_{safe_name}.pdf")
        try:
            generate_psychological_report(person, assessments, consultations, path)
            self.statusBar().showMessage(_t('psychological_records.report_generated', 'Exported') + f" → {path}", 3000)
        except Exception:
            self.statusBar().showMessage(_t('psychological_records.report_failed', 'Failed to export PDF'), 3000)

