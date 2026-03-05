"""
Material Design Theme Demo
Demonstrates both light and dark themes with automatic switching.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from src.ui.unified_main_window import UnifiedMainWindow
from unittest.mock import Mock


def create_demo_window():
    """Create window with mock database for demonstration."""
    window = UnifiedMainWindow()
    
    # Create mock database
    mock_db = Mock()
    mock_db.get_all_persons = Mock(return_value=[
        (1, "John Doe", "1234567890123", "2024-01-01"),
        (2, "Jane Smith", "9876543210987", "2024-01-02"),
        (3, "Alice Johnson", "1112223334445", "2024-01-03"),
        (4, "Bob Williams", "5556667778889", "2024-01-04"),
    ])
    mock_db.get_person_complete_record = Mock(return_value={
        "person": (1, "John Doe", "1234567890123", "2024-01-01"),
        "assessments": [
            (1, "2024-01-15", "Headache", "History of migraines", "Physical exam", "Migraine", "Ibuprofen", 1, "Follow-up in 2 weeks"),
            (2, "2024-02-01", "Anxiety", "Work-related stress", "Mental status exam", "Anxiety Disorder", "Therapy sessions", 1, "Continue treatment"),
        ],
        "consultations": [
            (1, "2024-01-20", "Follow-up", "Improved symptoms", "Good progress", "Ibuprofen 400mg", "Continue treatment", "2024-02-01", 1, "Patient responding well"),
            (2, "2024-02-05", "Telemedicine", "Stable condition", "No new concerns", "Same medication", "Monitor progress", "2024-03-01", 1, "Virtual consultation"),
        ],
    })
    mock_db.get_assessments_for_person = Mock(return_value=[
        (1, "2024-01-15", "Headache", "History", "Exam", "Migraine", "Treatment", 1, "Notes"),
        (2, "2024-02-01", "Anxiety", "History", "Exam", "Anxiety", "Therapy", 1, "Notes"),
    ])
    mock_db.get_consultations_for_person = Mock(return_value=[
        (1, "2024-01-20", "Follow-up", "Improved", "Progress", "Meds", "Continue", "2024-02-01", 1, "Good"),
        (2, "2024-02-05", "Telemedicine", "Stable", "No concerns", "Same", "Monitor", "2024-03-01", 1, "Virtual"),
    ])
    mock_db.add_person = Mock(return_value=True)
    mock_db.add_assessment = Mock(return_value=True)
    mock_db.add_consultation = Mock(return_value=True)
    
    window.db = mock_db
    window.attach_db_and_load()
    
    return window


def demo_with_timer(window):
    """Demo that automatically switches themes every 5 seconds."""
    def switch_theme():
        window.toggle_theme()
        print(f"Switched to {window.current_theme} mode")
    
    # Create timer for auto-switching
    timer = QTimer()
    timer.timeout.connect(switch_theme)
    timer.start(5000)  # Switch every 5 seconds
    
    # Show info message
    QMessageBox.information(
        window,
        "Theme Demo",
        "Welcome to the Material Design Theme Demo!\n\n"
        "The theme will automatically switch between Light and Dark modes every 5 seconds.\n\n"
        "You can also:\n"
        "• Click the theme button in the bottom-right corner\n"
        "• Press Ctrl+T to toggle manually\n\n"
        "Explore the application to see how all components adapt to both themes!"
    )
    
    return timer


def main():
    """Run the theme demo."""
    print("=" * 60)
    print("MATERIAL DESIGN THEME DEMO")
    print("=" * 60)
    print("\nStarting application with automatic theme switching...")
    print("Theme will switch every 5 seconds.")
    print("You can also press Ctrl+T to toggle manually.\n")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Psychological Records - Theme Demo")
    
    window = create_demo_window()
    timer = demo_with_timer(window)
    
    window.show()
    
    print(f"Initial theme: {window.current_theme}")
    print("\nApplication running. Close the window to exit.")
    
    result = app.exec()
    
    print("\nDemo completed.")
    return result


if __name__ == "__main__":
    sys.exit(main())

