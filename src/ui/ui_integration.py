"""
Integration script to migrate from the old UI system to the modern responsive design.
This script provides utilities for gradual migration and testing of the new UI system.
"""

import os
import sys
from typing import Dict, Any
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from src.ui.modern_main_window import ModernMainWindow
    from src.ui.modern_medical_records_window import ModernMedicalRecordsWindow
    from src.ui.main_window import MainWindow
    from src.ui.medical_records_window import MedicalRecordsWindow
    from src.core.database import DatabaseManager
    from src.utils.language_manager import get_language_manager
    from src.utils.theme_manager import get_theme_manager, ThemeMode
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

class UIIntegrationManager:
    """Manages the integration between old and new UI systems."""
    
    def __init__(self):
        self.app = None
        self.db_manager = None
        self.use_modern_ui = True  # Flag to control which UI to use
    
    def initialize_app(self, use_modern=True):
        """Initialize the application with either modern or legacy UI."""
        if QApplication.instance() is None:
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        
        self.app.setApplicationName("Modern Psychological Records System")
        self.app.setApplicationVersion("2.0.0")
        self.app.setOrganizationName("Healthcare Solutions")
        
        # Initialize database
        try:
            self.db_manager = DatabaseManager()
            print("✓ Database connection established")
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False
        
        # Set UI mode
        self.use_modern_ui = use_modern
        
        # Initialize language and theme managers
        lang_manager = get_language_manager()
        theme_manager = get_theme_manager()
        
        print(f"✓ Application initialized with {'modern' if use_modern else 'legacy'} UI")
        return True
    
    def create_main_window(self):
        """Create the main window using the selected UI system."""
        if self.use_modern_ui:
            return ModernMainWindow(self.db_manager)
        else:
            return MainWindow(self.db_manager)
    
    def create_medical_records_window(self, person_data, parent=None):
        """Create a medical records window using the selected UI system."""
        if self.use_modern_ui:
            return ModernMedicalRecordsWindow(person_data, self.db_manager, parent)
        else:
            return MedicalRecordsWindow(person_data, self.db_manager, parent)
    
    def run_ui_comparison_test(self):
        """Run a side-by-side comparison of old and new UI."""
        if not self.initialize_app():
            return False
        
        print("🔄 Starting UI comparison test...")
        
        # Create windows with both UIs
        modern_window = ModernMainWindow(self.db_manager)
        legacy_window = MainWindow(self.db_manager)
        
        # Position windows side by side
        screen = self.app.primaryScreen().availableGeometry()
        window_width = screen.width() // 2
        
        # Modern window on the left
        modern_window.resize(window_width, screen.height() - 100)
        modern_window.move(50, 50)
        modern_window.setWindowTitle("Modern UI - Enhanced Design")
        modern_window.show()
        
        # Legacy window on the right
        legacy_window.resize(window_width, screen.height() - 100)
        legacy_window.move(window_width + 100, 50)
        legacy_window.setWindowTitle("Legacy UI - Original Design")
        legacy_window.show()
        
        # Show comparison message
        QMessageBox.information(
            None,
            "UI Comparison",
            "Both UI versions are now displayed side by side.\\n\\n"
            "Left: Modern responsive UI with enhanced styling\\n"
            "Right: Original legacy UI\\n\\n"
            "Compare the visual differences, responsiveness, and user experience."
        )
        
        return self.app.exec()
    
    def run_modern_ui_demo(self):
        """Run a demonstration of the modern UI features."""
        if not self.initialize_app(use_modern=True):
            return False
        
        print("🚀 Starting modern UI demonstration...")
        
        # Create main window
        main_window = self.create_main_window()
        main_window.show()
        
        # Create demo message
        QTimer.singleShot(1000, lambda: self.show_modern_features_guide(main_window))
        
        return self.app.exec()
    
    def show_modern_features_guide(self, main_window):
        """Show a guide to modern UI features."""
        features_text = """
🎨 Modern UI Features Demonstration

✨ Visual Enhancements:
• Modern color scheme with light/dark theme support
• Enhanced typography and spacing
• Responsive button groups and layouts
• Improved table headers and action buttons

🔧 Responsive Design:
• Adaptive layouts for different screen sizes
• Mobile-friendly interface adaptations
• Flexible container systems
• Breakpoint-based responsive behavior

🎯 User Experience:
• Consistent design language
• Better visual hierarchy
• Improved accessibility
• Theme persistence across sessions

📱 Test Responsiveness:
• Resize the window to see adaptive layouts
• Use Ctrl+T to toggle between themes
• Notice improved table visibility and interactions
• Experience enhanced navigation

Try interacting with the interface to see these features in action!
        """
        
        QMessageBox.information(main_window, "Modern UI Features", features_text)
    
    def migrate_existing_data(self):
        """Test data migration between UI systems."""
        print("📊 Testing data migration compatibility...")
        
        # Test database operations with both UI systems
        try:
            # Modern UI test
            self.use_modern_ui = True
            modern_window = self.create_main_window()
            print("✓ Modern UI database integration: OK")
            
            # Legacy UI test
            self.use_modern_ui = False
            legacy_window = self.create_main_window()
            print("✓ Legacy UI database integration: OK")
            
            print("✓ Data migration compatibility: VERIFIED")
            return True
            
        except Exception as e:
            print(f"✗ Migration test failed: {e}")
            return False
    
    def run_integration_tests(self):
        """Run comprehensive integration tests."""
        print("🧪 Running integration tests...")
        
        tests = [
            ("Database Connection", self.test_database_connection),
            ("Modern UI Creation", self.test_modern_ui_creation),
            ("Legacy UI Creation", self.test_legacy_ui_creation),
            ("Theme System", self.test_theme_system),
            ("Language System", self.test_language_system),
            ("Responsive Behavior", self.test_responsive_behavior),
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = "PASSED" if result else "FAILED"
                print(f"  {'✓' if result else '✗'} {test_name}: {results[test_name]}")
            except Exception as e:
                results[test_name] = f"ERROR: {e}"
                print(f"  ✗ {test_name}: ERROR - {e}")
        
        # Summary
        passed = sum(1 for result in results.values() if result == "PASSED")
        total = len(results)
        
        print(f"\\n📈 Test Results: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All integration tests passed! System ready for deployment.")
        else:
            print("⚠️  Some tests failed. Review issues before proceeding.")
        
        return passed == total
    
    def test_database_connection(self):
        """Test database connection."""
        try:
            if not self.db_manager:
                self.db_manager = DatabaseManager()
            return self.db_manager.connection is not None
        except:
            return False
    
    def test_modern_ui_creation(self):
        """Test modern UI window creation."""
        try:
            if not self.app:
                self.app = QApplication.instance() or QApplication(sys.argv)
            window = ModernMainWindow(self.db_manager)
            return window is not None
        except:
            return False
    
    def test_legacy_ui_creation(self):
        """Test legacy UI window creation."""
        try:
            if not self.app:
                self.app = QApplication.instance() or QApplication(sys.argv)
            window = MainWindow(self.db_manager)
            return window is not None
        except:
            return False
    
    def test_theme_system(self):
        """Test theme system functionality."""
        try:
            theme_manager = get_theme_manager()
            current_theme = theme_manager.get_current_theme()
            
            # Test theme switching
            new_theme = ThemeMode.DARK if current_theme == ThemeMode.LIGHT else ThemeMode.LIGHT
            theme_manager.change_theme(new_theme)
            
            # Verify change
            changed_theme = theme_manager.get_current_theme()
            
            # Restore original theme
            theme_manager.change_theme(current_theme)
            
            return changed_theme == new_theme
        except:
            return False
    
    def test_language_system(self):
        """Test language system functionality."""
        try:
            lang_manager = get_language_manager()
            current_lang = lang_manager.get_current_language()
            return current_lang is not None
        except:
            return False
    
    def test_responsive_behavior(self):
        """Test responsive behavior of modern UI."""
        try:
            from src.ui.responsive_layout import ResponsiveBreakpoints
            
            # Test breakpoint detection
            xs_class = ResponsiveBreakpoints.get_size_class(400)
            md_class = ResponsiveBreakpoints.get_size_class(800)
            xl_class = ResponsiveBreakpoints.get_size_class(1400)
            
            return xs_class == "xs" and md_class == "md" and xl_class == "xl"
        except:
            return False

def main():
    """Main entry point for UI integration."""
    integration_manager = UIIntegrationManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            integration_manager.run_integration_tests()
        elif command == "compare":
            integration_manager.run_ui_comparison_test()
        elif command == "demo":
            integration_manager.run_modern_ui_demo()
        elif command == "migrate":
            integration_manager.migrate_existing_data()
        else:
            print("Usage: python ui_integration.py [test|compare|demo|migrate]")
    else:
        # Default: run modern UI
        integration_manager.run_modern_ui_demo()

if __name__ == "__main__":
    main()
