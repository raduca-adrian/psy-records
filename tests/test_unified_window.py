"""
Tests for the unified single-window application.
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui.unified_main_window import UnifiedMainWindow


@pytest.fixture
def qapp():
    """Create QApplication instance for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


@pytest.fixture
def mock_db():
    """Create a mock database manager."""
    db = Mock()
    db.get_all_persons = Mock(return_value=[
        (1, "John Doe", "1234567890123", "2024-01-01"),
        (2, "Jane Smith", "9876543210987", "2024-01-02"),
    ])
    db.get_person_complete_record = Mock(return_value={
        "person": (1, "John Doe", "1234567890123", "2024-01-01"),
        "assessments": [],
        "consultations": [],
    })
    db.get_assessments_for_person = Mock(return_value=[])
    db.get_consultations_for_person = Mock(return_value=[])
    db.add_person = Mock(return_value=True)
    db.add_assessment = Mock(return_value=True)
    db.add_consultation = Mock(return_value=True)
    db.update_assessment = Mock(return_value=True)
    db.update_consultation = Mock(return_value=True)
    return db


@pytest.fixture
def window(qapp, mock_db):
    """Create UnifiedMainWindow instance with mock database."""
    win = UnifiedMainWindow()
    win.db = mock_db
    win.attach_db_and_load()
    return win


def test_window_creation(window):
    """Test that the window is created successfully."""
    assert window is not None
    assert window.windowTitle() == "Psychological Records"
    assert window.minimumWidth() == 1200
    assert window.minimumHeight() == 700


def test_tabs_exist(window):
    """Test that all required tabs exist."""
    assert window.tabs.count() == 4
    # Check tab titles
    tab_titles = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert "Patients" in tab_titles[0]
    assert "Add Patient" in tab_titles[1]
    assert "Checkup" in tab_titles[2]
    assert "Session" in tab_titles[3]


def test_patients_loaded(window, mock_db):
    """Test that patients are loaded into the table."""
    assert window.table.rowCount() == 2
    # Check first patient
    assert window.table.item(0, 0).text() == "1"
    assert window.table.item(0, 1).text() == "John Doe"
    assert window.table.item(0, 2).text() == "1234567890123"


def test_patient_selection(window, mock_db):
    """Test patient selection updates the records view."""
    # Select first patient
    window.table.selectRow(0)
    assert window.current_patient_id == 1
    assert "John Doe" in window.records_view.toPlainText()


def test_add_patient_tab_switch(window):
    """Test switching to add patient tab."""
    window.tabs.setCurrentIndex(1)
    assert window.tabs.currentIndex() == 1
    assert window.patient_name_edit is not None
    assert window.patient_cnp_edit is not None


def test_clear_patient_form(window):
    """Test clearing the patient form."""
    window.patient_name_edit.setText("Test Patient")
    window.patient_cnp_edit.setText("1234567890123")
    window.clear_patient_form()
    assert window.patient_name_edit.text() == ""
    assert window.patient_cnp_edit.text() == ""


def test_save_patient(window, mock_db):
    """Test saving a new patient."""
    window.patient_name_edit.setText("New Patient")
    window.patient_cnp_edit.setText("1111111111111")
    window.save_patient()
    # Verify database was called
    mock_db.add_person.assert_called_once_with("New Patient", "1111111111111")


def test_start_add_checkup_no_patient(window, qapp):
    """Test starting add checkup without patient selected."""
    window.current_patient_id = None
    window.start_add_checkup()
    # Should show warning and not switch tabs
    assert window.tabs.currentIndex() == 0


def test_start_add_checkup_with_patient(window, mock_db):
    """Test starting add checkup with patient selected."""
    window.current_patient_id = 1
    window.start_add_checkup()
    # Should switch to checkup tab
    assert window.tabs.currentIndex() == 2
    assert window.checkup_edit_mode == False
    assert "John Doe" in window.checkup_patient_label.text()


def test_clear_checkup_form(window):
    """Test clearing the checkup form."""
    window.checkup_chief_edit.setText("Test complaint")
    window.checkup_diagnosis_edit.setPlainText("Test diagnosis")
    window.clear_checkup_form()
    assert window.checkup_chief_edit.text() == ""
    assert window.checkup_diagnosis_edit.toPlainText() == ""


def test_start_add_session_no_patient(window):
    """Test starting add session without patient selected."""
    window.current_patient_id = None
    window.start_add_session()
    # Should show warning and not switch tabs
    assert window.tabs.currentIndex() == 0


def test_start_add_session_with_patient(window, mock_db):
    """Test starting add session with patient selected."""
    window.current_patient_id = 1
    window.start_add_session()
    # Should switch to session tab
    assert window.tabs.currentIndex() == 3
    assert window.session_edit_mode == False
    assert "John Doe" in window.session_patient_label.text()


def test_clear_session_form(window):
    """Test clearing the session form."""
    window.session_symptoms_edit.setPlainText("Test symptoms")
    window.session_findings_edit.setPlainText("Test findings")
    window.clear_session_form()
    assert window.session_symptoms_edit.toPlainText() == ""
    assert window.session_findings_edit.toPlainText() == ""


def test_refresh_patients(window, mock_db):
    """Test refreshing the patient list."""
    # Modify mock to return different data
    mock_db.get_all_persons.return_value = [
        (1, "Updated Patient", "1234567890123", "2024-01-01"),
    ]
    window.refresh_patients()
    # Verify table updated
    assert window.table.rowCount() == 1
    assert window.table.item(0, 1).text() == "Updated Patient"


def test_keyboard_shortcuts_exist(window):
    """Test that keyboard shortcuts are set up."""
    # Just verify the window has shortcuts
    # (actual shortcut testing would require QTest)
    assert hasattr(window, '_setup_shortcuts')


def test_styling_applied(window):
    """Test that styling is applied."""
    assert window.styleSheet() != ""
    assert "QMainWindow" in window.styleSheet()
    assert "QTabWidget" in window.styleSheet()


def test_status_bar_exists(window):
    """Test that status bar exists and shows messages."""
    assert window.statusBar() is not None
    window.statusBar().showMessage("Test message")
    assert window.statusBar().currentMessage() == "Test message"


def test_table_headers(window):
    """Test that table has correct headers."""
    headers = [window.table.horizontalHeaderItem(i).text() 
               for i in range(window.table.columnCount())]
    assert "ID" in headers
    assert "Name" in headers
    assert "CNP" in headers


def test_edit_mode_flags(window):
    """Test that edit mode flags are initialized correctly."""
    assert window.checkup_edit_mode == False
    assert window.checkup_edit_id is None
    assert window.session_edit_mode == False
    assert window.session_edit_id is None


def test_current_patient_tracking(window):
    """Test that current patient ID is tracked correctly."""
    assert window.current_patient_id is None
    window.table.selectRow(0)
    assert window.current_patient_id == 1
    window.table.clearSelection()
    window.load_records_for_selected()
    assert window.current_patient_id is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

