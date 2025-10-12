"""
Manual test script for the unified window application.
Run this to verify basic functionality.
"""

import sys
import os
from unittest.mock import Mock

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

# Mock PyQt6 if needed for basic testing
try:
    from PyQt6.QtWidgets import QApplication
    from src.ui.unified_main_window import UnifiedMainWindow
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("PyQt6 not available for full UI testing")


def create_mock_db():
    """Create a mock database for testing."""
    db = Mock()
    db.get_all_persons = Mock(return_value=[
        (1, "John Doe", "1234567890123", "2024-01-01"),
        (2, "Jane Smith", "9876543210987", "2024-01-02"),
    ])
    db.get_person_complete_record = Mock(return_value={
        "person": (1, "John Doe", "1234567890123", "2024-01-01"),
        "assessments": [(1, "2024-01-15", "Headache", "History", "Exam", "Migraine", "Treatment", 1, "Notes")],
        "consultations": [(1, "2024-01-20", "Follow-up", "Improved", "Good progress", "Ibuprofen", "Continue", "2024-02-01", 1, "Follow-up notes")],
    })
    db.get_assessments_for_person = Mock(return_value=[
        (1, "2024-01-15", "Headache", "History", "Exam", "Migraine", "Treatment", 1, "Notes")
    ])
    db.get_consultations_for_person = Mock(return_value=[
        (1, "2024-01-20", "Follow-up", "Improved", "Good progress", "Ibuprofen", "Continue", "2024-02-01", 1, "Notes")
    ])
    db.add_person = Mock(return_value=True)
    db.add_assessment = Mock(return_value=True)
    db.add_consultation = Mock(return_value=True)
    db.update_assessment = Mock(return_value=True)
    db.update_consultation = Mock(return_value=True)
    return db


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        from src.ui.unified_main_window import UnifiedMainWindow
        print("✓ UnifiedMainWindow imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import UnifiedMainWindow: {e}")
        return False


def test_window_creation():
    """Test window creation with mock database."""
    if not PYQT_AVAILABLE:
        print("Skipping window creation test (PyQt6 not available)")
        return True
        
    print("\nTesting window creation...")
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            
        window = UnifiedMainWindow()
        print("✓ Window created successfully")
        
        # Test tabs
        tab_count = window.tabs.count()
        if tab_count == 4:
            print(f"✓ All 4 tabs created successfully")
        else:
            print(f"✗ Expected 4 tabs, got {tab_count}")
            return False
            
        # Test with mock database
        mock_db = create_mock_db()
        window.db = mock_db
        window.attach_db_and_load()
        print("✓ Database attached and data loaded")
        
        # Test table population
        row_count = window.table.rowCount()
        if row_count == 2:
            print(f"✓ Patient table populated with {row_count} rows")
        else:
            print(f"✗ Expected 2 rows, got {row_count}")
            return False
            
        # Test patient selection
        window.table.selectRow(0)
        if window.current_patient_id == 1:
            print("✓ Patient selection working")
        else:
            print(f"✗ Expected patient ID 1, got {window.current_patient_id}")
            return False
            
        # Test form fields exist
        assert hasattr(window, 'patient_name_edit')
        assert hasattr(window, 'checkup_chief_edit')
        assert hasattr(window, 'session_symptoms_edit')
        print("✓ All form fields exist")
        
        # Test keyboard shortcuts setup
        assert hasattr(window, '_setup_shortcuts')
        print("✓ Keyboard shortcuts configured")
        
        # Test styling applied
        if window.styleSheet():
            print("✓ Styling applied")
        else:
            print("✗ No styling applied")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Window creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_functionality():
    """Test basic functionality."""
    if not PYQT_AVAILABLE:
        print("Skipping functionality test (PyQt6 not available)")
        return True
        
    print("\nTesting functionality...")
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
            
        window = UnifiedMainWindow()
        mock_db = create_mock_db()
        window.db = mock_db
        window.attach_db_and_load()
        
        # Test tab switching
        window.tabs.setCurrentIndex(1)
        if window.tabs.currentIndex() == 1:
            print("✓ Tab switching works")
        else:
            print("✗ Tab switching failed")
            return False
            
        # Test form clearing
        window.patient_name_edit.setText("Test")
        window.clear_patient_form()
        if window.patient_name_edit.text() == "":
            print("✓ Form clearing works")
        else:
            print("✗ Form clearing failed")
            return False
            
        # Test patient selection workflow
        window.tabs.setCurrentIndex(0)
        window.table.selectRow(0)
        window.start_add_checkup()
        if window.tabs.currentIndex() == 2:
            print("✓ Add checkup workflow works")
        else:
            print("✗ Add checkup workflow failed")
            return False
            
        # Test session workflow
        window.tabs.setCurrentIndex(0)
        window.table.selectRow(0)
        window.start_add_session()
        if window.tabs.currentIndex() == 3:
            print("✓ Add session workflow works")
        else:
            print("✗ Add session workflow failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("UNIFIED WINDOW APPLICATION TESTS")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Window Creation Test", test_window_creation()))
    results.append(("Functionality Test", test_functionality()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The unified window application is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

